#!/usr/bin/env bash

# Ubuntu 24.04 环境安装脚本
# 安装: Python 3.13, Node.js, npm, MongoDB, Redis
# 使用方法: chmod +x setup_env_ubuntu24.sh && ./setup_env_ubuntu24.sh

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为 root 用户
check_user() {
    if [[ $EUID -eq 0 ]]; then
        log_error "请不要使用 root 用户运行此脚本，使用普通用户即可"
        exit 1
    fi
}

# 检查 Ubuntu 版本
check_ubuntu_version() {
    log_info "检查 Ubuntu 版本..."
    if ! grep -q "Ubuntu 24.04" /etc/os-release; then
        log_warning "此脚本专为 Ubuntu 24.04 设计，当前系统可能不兼容"
        read -p "是否继续? (y/N): " -r
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    log_success "Ubuntu 版本检查完成"
}

# 更新系统并安装基础依赖
install_base_packages() {
    log_info "更新系统并安装基础依赖包..."
    
    sudo apt-get update
    sudo apt-get upgrade -y
    
    sudo apt-get install -y \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        curl \
        wget \
        gnupg \
        lsb-release \
        build-essential \
        git \
        vim \
        htop \
        ufw \
        net-tools
        
    log_success "基础依赖包安装完成"
}

# 安装 Python 3.13
install_python() {
    log_info "安装 Python 3.13..."
    
    # 添加 deadsnakes PPA
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt-get update
    
    # 安装 Python 3.13 及相关包
    sudo apt-get install -y \
        python3.13 \
        python3.13-venv \
        python3.13-dev \
        python3.13-distutils \
        python3-pip
    
    # 验证安装
    if command -v python3.13 &> /dev/null; then
        PYTHON_VERSION=$(python3.13 --version)
        log_success "Python 安装成功: $PYTHON_VERSION"
        
        # 创建符号链接（可选）
        if ! command -v python3 &> /dev/null || [[ $(python3 --version) != *"3.13"* ]]; then
            log_info "创建 python3 -> python3.13 符号链接..."
            sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 1
        fi
    else
        log_error "Python 3.13 安装失败"
        exit 1
    fi
}

# 安装 Node.js 和 npm (使用 NodeSource 官方源)
install_nodejs() {
    log_info "安装 Node.js 和 npm (最新 LTS 版本)..."
    
    # 添加 NodeSource 官方仓库
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    
    # 安装 Node.js (包含 npm)
    sudo apt-get install -y nodejs
    
    # 验证安装
    if command -v node &> /dev/null && command -v npm &> /dev/null; then
        NODE_VERSION=$(node --version)
        NPM_VERSION=$(npm --version)
        log_success "Node.js 安装成功: $NODE_VERSION"
        log_success "npm 安装成功: $NPM_VERSION"
    else
        log_error "Node.js/npm 安装失败"
        exit 1
    fi
}

# 安装 MongoDB
install_mongodb() {
    log_info "安装 MongoDB 5.0..."
    
    # 导入 MongoDB 公钥
    wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
    
    # Ubuntu 24.04 使用 jammy，但 MongoDB 5.0 可能只有 focal，先尝试 jammy
    UBUNTU_CODENAME=$(lsb_release -cs)
    if [[ "$UBUNTU_CODENAME" == "noble" ]]; then
        # Ubuntu 24.04 noble，但 MongoDB 可能没有 noble 源，使用 jammy
        MONGO_CODENAME="jammy"
    else
        MONGO_CODENAME="$UBUNTU_CODENAME"
    fi
    
    log_info "使用 MongoDB 源: $MONGO_CODENAME"
    
    # 创建 MongoDB 源列表文件
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $MONGO_CODENAME/mongodb-org/5.0 multiverse" \
        | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
    
    # 如果 jammy 源不存在，fallback 到 focal
    sudo apt-get update || {
        log_warning "jammy 源不可用，使用 focal 源"
        echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" \
            | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
        sudo apt-get update
    }
    
    # 安装 MongoDB
    sudo apt-get install -y mongodb-org
    
    # 启动服务
    sudo systemctl daemon-reload
    sudo systemctl start mongod
    sudo systemctl enable mongod
    
    # 等待服务启动
    log_info "等待 MongoDB 服务启动..."
    sleep 5
    
    # 验证服务状态
    if sudo systemctl is-active --quiet mongod; then
        log_success "MongoDB 服务启动成功"
    else
        log_error "MongoDB 服务启动失败"
        sudo systemctl status mongod
        exit 1
    fi
}

# 配置 MongoDB 用户
configure_mongodb() {
    log_info "配置 MongoDB 管理员用户..."
    
    # 等待 MongoDB 完全启动
    local retry_count=0
    while ! mongosh --eval "db.runCommand('ping')" &> /dev/null; do
        if [[ $retry_count -gt 30 ]]; then
            log_error "MongoDB 连接超时"
            exit 1
        fi
        log_info "等待 MongoDB 完全启动... ($retry_count/30)"
        sleep 2
        ((retry_count++))
    done
    
    # 创建管理员用户（如果不存在）
    mongosh --eval "
        try {
            use admin
            db.createUser({
                user: 'admin',
                pwd: 'tradingagents123',
                roles: ['userAdminAnyDatabase', 'dbAdminAnyDatabase', 'readWriteAnyDatabase']
            })
            print('MongoDB 管理员用户创建成功')
        } catch (e) {
            if (e.code === 11000) {
                print('MongoDB 管理员用户已存在')
            } else {
                print('创建用户失败:', e.message)
            }
        }
    " || log_warning "MongoDB 用户配置可能已存在或失败"
    
    log_success "MongoDB 配置完成"
}

# 配置 MongoDB 网络访问
configure_mongodb_network() {
    log_info "配置 MongoDB 网络访问..."
    
    local mongo_conf="/etc/mongod.conf"
    
    # 备份原配置文件
    sudo cp "$mongo_conf" "$mongo_conf.backup.$(date +%Y%m%d_%H%M%S)"
    
    # 配置网络绑定 - 允许所有IP访问 (生产环境建议限制具体IP)
    if grep -q "^  bindIp:" "$mongo_conf"; then
        sudo sed -i 's/^  bindIp:.*/  bindIp: 0.0.0.0/' "$mongo_conf"
    elif grep -q "^#  bindIp:" "$mongo_conf"; then
        sudo sed -i 's/^#  bindIp:.*/  bindIp: 0.0.0.0/' "$mongo_conf"
    else
        # 在 net: 部分添加 bindIp 配置
        sudo sed -i '/^net:/a\  bindIp: 0.0.0.0' "$mongo_conf"
    fi
    
    # 确保端口配置正确
    if ! grep -q "^  port:" "$mongo_conf"; then
        sudo sed -i '/^net:/a\  port: 27017' "$mongo_conf"
    fi
    
    # 重启 MongoDB
    sudo systemctl restart mongod
    
    # 验证网络绑定
    sleep 3
    if netstat -tlnp | grep :27017 | grep -q "0.0.0.0:27017"; then
        log_success "MongoDB 网络访问配置成功 (0.0.0.0:27017)"
    else
        log_warning "MongoDB 网络绑定可能未完全生效，请检查配置"
    fi
}

# 安装 Redis
install_redis() {
    log_info "安装 Redis..."
    
    sudo apt-get update
    sudo apt-get install -y redis-server
    
    # 启动服务
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
    
    # 验证服务状态
    if sudo systemctl is-active --quiet redis-server; then
        log_success "Redis 服务启动成功"
    else
        log_error "Redis 服务启动失败"
        sudo systemctl status redis-server
        exit 1
    fi
}

# 配置 Redis 密码
configure_redis() {
    log_info "配置 Redis 密码..."
    
    local redis_conf="/etc/redis/redis.conf"
    
    # 备份原配置文件
    sudo cp "$redis_conf" "$redis_conf.backup.$(date +%Y%m%d_%H%M%S)"
    
    # 设置密码
    if grep -q "^requirepass" "$redis_conf"; then
        sudo sed -i 's/^requirepass .*/requirepass tradingagents123/' "$redis_conf"
    elif grep -q "^# requirepass" "$redis_conf"; then
        sudo sed -i 's/^# requirepass .*/requirepass tradingagents123/' "$redis_conf"
    else
        echo 'requirepass tradingagents123' | sudo tee -a "$redis_conf" > /dev/null
    fi
    
    # 配置网络绑定 - 允许所有IP访问 (生产环境建议限制具体IP)
    if grep -q "^bind " "$redis_conf"; then
        sudo sed -i 's/^bind .*/bind 0.0.0.0/' "$redis_conf"
    elif grep -q "^# bind " "$redis_conf"; then
        sudo sed -i 's/^# bind .*/bind 0.0.0.0/' "$redis_conf"
    else
        echo 'bind 0.0.0.0' | sudo tee -a "$redis_conf" > /dev/null
    fi
    
    # 禁用保护模式以允许远程连接
    if grep -q "^protected-mode" "$redis_conf"; then
        sudo sed -i 's/^protected-mode .*/protected-mode no/' "$redis_conf"
    elif grep -q "^# protected-mode" "$redis_conf"; then
        sudo sed -i 's/^# protected-mode .*/protected-mode no/' "$redis_conf"
    else
        echo 'protected-mode no' | sudo tee -a "$redis_conf" > /dev/null
    fi
    
    # 重启 Redis
    sudo systemctl restart redis-server
    
    # 验证密码配置和网络绑定
    sleep 3
    if redis-cli -a tradingagents123 ping | grep -q "PONG"; then
        log_success "Redis 密码配置成功"
    else
        log_error "Redis 密码配置失败"
        exit 1
    fi
    
    # 验证网络绑定
    if netstat -tlnp | grep :6379 | grep -q "0.0.0.0:6379"; then
        log_success "Redis 网络访问配置成功 (0.0.0.0:6379)"
    else
        log_warning "Redis 网络绑定可能未完全生效，请检查配置"
    fi
}

# 配置防火墙和端口开放
configure_firewall() {
    log_info "配置防火墙和开放端口..."
    
    # 启用 UFW 防火墙
    sudo ufw --force enable
    
    # 允许 SSH (22) - 避免锁定自己
    sudo ufw allow ssh
    sudo ufw allow 22/tcp
    
    # 开放 MongoDB 端口 (27017)
    sudo ufw allow 27017/tcp
    log_info "已开放 MongoDB 端口: 27017"
    
    # 开放 Redis 端口 (6379)
    sudo ufw allow 6379/tcp
    log_info "已开放 Redis 端口: 6379"
    
    # 开放额外端口 (3000) - 通常用于前端开发服务器
    sudo ufw allow 3000/tcp
    log_info "已开放开发端口: 3000"
    
    # 显示防火墙状态
    log_info "当前防火墙规则:"
    sudo ufw status numbered
    
    log_success "防火墙配置完成"
}

# 显示网络访问信息
show_network_info() {
    log_info "获取网络访问信息..."
    
    # 获取本机IP地址
    local internal_ip=$(hostname -I | awk '{print $1}')
    local external_ip=$(curl -s -m 5 ifconfig.me 2>/dev/null || echo "无法获取")
    
    echo
    echo "=== 网络访问信息 ==="
    echo "内网IP: $internal_ip"
    echo "外网IP: $external_ip"
    echo
    echo "服务端口状态:"
    echo "  MongoDB (27017): $(netstat -tlnp | grep :27017 | awk '{print $4}' || echo '未启动')"
    echo "  Redis (6379):    $(netstat -tlnp | grep :6379 | awk '{print $4}' || echo '未启动')"
    echo "  开发端口 (3000): 已开放（待应用使用）"
    echo
}

# 验证所有服务
verify_services() {
    log_info "验证所有服务状态..."
    
    echo
    echo "=== 服务验证结果 ==="
    
    # Python
    if command -v python3.13 &> /dev/null; then
        echo -e "${GREEN}✓${NC} Python: $(python3.13 --version)"
    else
        echo -e "${RED}✗${NC} Python: 未安装"
    fi
    
    # Node.js
    if command -v node &> /dev/null; then
        echo -e "${GREEN}✓${NC} Node.js: $(node --version)"
    else
        echo -e "${RED}✗${NC} Node.js: 未安装"
    fi
    
    # npm
    if command -v npm &> /dev/null; then
        echo -e "${GREEN}✓${NC} npm: $(npm --version)"
    else
        echo -e "${RED}✗${NC} npm: 未安装"
    fi
    
    # MongoDB
    if sudo systemctl is-active --quiet mongod; then
        local mongo_version=$(mongosh --eval "db.version()" --quiet 2>/dev/null || echo "未知版本")
        echo -e "${GREEN}✓${NC} MongoDB: 运行中 ($mongo_version)"
        
        # 测试连接
        if mongosh --eval "db.runCommand('ping')" &> /dev/null; then
            echo -e "${GREEN}✓${NC} MongoDB: 连接正常"
        else
            echo -e "${YELLOW}!${NC} MongoDB: 连接异常"
        fi
    else
        echo -e "${RED}✗${NC} MongoDB: 未运行"
    fi
    
    # Redis
    if sudo systemctl is-active --quiet redis-server; then
        local redis_version=$(redis-server --version | head -n1)
        echo -e "${GREEN}✓${NC} Redis: 运行中 ($redis_version)"
        
        # 测试连接
        if redis-cli -a tradingagents123 ping | grep -q "PONG" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} Redis: 连接正常 (密码: tradingagents123)"
        else
            echo -e "${YELLOW}!${NC} Redis: 连接异常"
        fi
    else
        echo -e "${RED}✗${NC} Redis: 未运行"
    fi
    
    echo
}

# 输出使用说明
show_usage_info() {
    echo "=== 使用说明 ==="
    echo
    echo "连接信息:"
    echo "  本地 MongoDB: mongodb://admin:tradingagents123@localhost:27017/"
    echo "  远程 MongoDB: mongodb://admin:tradingagents123@<SERVER_IP>:27017/"
    echo "  本地 Redis:   redis://:tradingagents123@localhost:6379"
    echo "  远程 Redis:   redis://:tradingagents123@<SERVER_IP>:6379"
    echo "  开发服务器:   http://localhost:3000 或 http://<SERVER_IP>:3000"
    echo
    echo "常用命令:"
    echo "  查看服务状态: sudo systemctl status mongod redis-server"
    echo "  重启服务:     sudo systemctl restart mongod redis-server"
    echo "  MongoDB连接:  mongosh mongodb://admin:tradingagents123@localhost:27017/"
    echo "  Redis连接:    redis-cli -a tradingagents123"
    echo "  查看端口状态: sudo netstat -tlnp | grep -E ':(27017|6379|3000)'"
    echo "  防火墙状态:   sudo ufw status"
    echo "  开放新端口:   sudo ufw allow <PORT>/tcp"
    echo
    echo "Python 虚拟环境创建:"
    echo "  python3.13 -m venv venv"
    echo "  source venv/bin/activate"
    echo
}

# 主函数
main() {
    echo "=== Ubuntu 24.04 开发环境安装脚本 ==="
    echo "安装: Python 3.13, Node.js, npm, MongoDB, Redis"
    echo
    
    check_user
    check_ubuntu_version
    
    echo
    read -p "是否开始安装? (Y/n): " -r
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
    
    echo
    install_base_packages
    install_python
    install_nodejs
    install_mongodb
    configure_mongodb
    configure_mongodb_network
    install_redis
    configure_redis
    configure_firewall
    
    echo
    verify_services
    show_network_info
    show_usage_info
    
    log_success "所有组件安装配置完成！"
}

# 错误处理
trap 'log_error "脚本执行失败，请检查上方错误信息"; exit 1' ERR

# 执行主函数
main "$@"
