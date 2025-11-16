"""
债券数据同步任务测试
测试定时同步任务的功能
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
import pandas as pd


@pytest.mark.asyncio
async def test_sync_cov_comparison_success():
    """测试可转债比价表同步成功"""
    from app.worker.bonds_sync_service import BondSyncService
    
    # Mock AKShare Provider
    with patch('app.worker.bonds_sync_service.AKShareBondProvider') as mock_provider_class:
        # Mock Provider实例
        mock_provider = Mock()
        mock_df = pd.DataFrame([
            {"转债代码": "113682", "转债名称": "益丰转债", "转债最新价": 120.5}
        ])
        mock_provider.get_cov_comparison = AsyncMock(return_value=mock_df)
        mock_provider_class.return_value = mock_provider
        
        # Mock MongoDB
        with patch('app.worker.bonds_sync_service.get_mongo_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            # Mock BondDataService
            with patch('app.worker.bonds_sync_service.BondDataService') as mock_service_class:
                mock_service = Mock()
                mock_service.ensure_indexes = AsyncMock()
                mock_service.save_cov_comparison = AsyncMock(return_value=1)
                mock_service_class.return_value = mock_service
                
                # 执行同步
                sync_service = BondSyncService()
                result = await sync_service.sync_cov_comparison()
                
                # 验证
                assert result["success"] is True
                assert result["saved"] == 1
                assert result["rows"] == 1
                
                # 验证方法被调用
                assert mock_provider.get_cov_comparison.called
                assert mock_service.save_cov_comparison.called
    
    print("✅ 测试通过：可转债比价表同步成功")


@pytest.mark.asyncio
async def test_sync_cov_comparison_empty_data():
    """测试同步空数据"""
    from app.worker.bonds_sync_service import BondSyncService
    
    # Mock返回空DataFrame
    with patch('app.worker.bonds_sync_service.AKShareBondProvider') as mock_provider_class:
        mock_provider = Mock()
        mock_provider.get_cov_comparison = AsyncMock(return_value=pd.DataFrame())
        mock_provider_class.return_value = mock_provider
        
        with patch('app.worker.bonds_sync_service.get_mongo_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            with patch('app.worker.bonds_sync_service.BondDataService') as mock_service_class:
                mock_service = Mock()
                mock_service.ensure_indexes = AsyncMock()
                mock_service_class.return_value = mock_service
                
                # 执行同步
                sync_service = BondSyncService()
                result = await sync_service.sync_cov_comparison()
                
                # 验证
                assert result["success"] is True
                assert result["saved"] == 0
                assert result["rows"] == 0
                
                # 保存方法不应被调用
                assert not mock_service.save_cov_comparison.called
    
    print("✅ 测试通过：同步空数据")


@pytest.mark.asyncio
async def test_sync_cov_comparison_error():
    """测试同步时发生错误"""
    from app.worker.bonds_sync_service import BondSyncService
    
    # Mock抛出异常
    with patch('app.worker.bonds_sync_service.AKShareBondProvider') as mock_provider_class:
        mock_provider = Mock()
        mock_provider.get_cov_comparison = AsyncMock(side_effect=Exception("网络错误"))
        mock_provider_class.return_value = mock_provider
        
        with patch('app.worker.bonds_sync_service.get_mongo_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            with patch('app.worker.bonds_sync_service.BondDataService') as mock_service_class:
                mock_service = Mock()
                mock_service.ensure_indexes = AsyncMock()
                mock_service_class.return_value = mock_service
                
                # 执行同步
                sync_service = BondSyncService()
                result = await sync_service.sync_cov_comparison()
                
                # 验证错误被正确处理
                assert result["success"] is False
                assert "error" in result
                assert "网络错误" in result["error"]
    
    print("✅ 测试通过：同步错误处理")


@pytest.mark.asyncio
async def test_sync_spot_deals_success():
    """测试现券成交行情同步成功"""
    from app.worker.bonds_sync_service import BondSyncService
    
    # Mock Provider
    with patch('app.worker.bonds_sync_service.AKShareBondProvider') as mock_provider_class:
        mock_provider = Mock()
        mock_df = pd.DataFrame([
            {"债券简称": "23附息国债26", "成交净价": 103.20}
        ])
        mock_provider.get_spot_deal = AsyncMock(return_value=mock_df)
        mock_provider_class.return_value = mock_provider
        
        with patch('app.worker.bonds_sync_service.get_mongo_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            with patch('app.worker.bonds_sync_service.BondDataService') as mock_service_class:
                mock_service = Mock()
                mock_service.ensure_indexes = AsyncMock()
                mock_service.save_spot_deals = AsyncMock(return_value=1)
                mock_service_class.return_value = mock_service
                
                # 执行同步
                sync_service = BondSyncService()
                result = await sync_service.sync_spot_deals()
                
                # 验证
                assert result["success"] is True
                assert result["saved"] == 1
                assert result["rows"] == 1
    
    print("✅ 测试通过：现券成交行情同步成功")


@pytest.mark.asyncio
async def test_sync_market_summary_success():
    """测试市场概览同步成功"""
    from app.worker.bonds_sync_service import BondSyncService
    
    # Mock Provider
    with patch('app.worker.bonds_sync_service.AKShareBondProvider') as mock_provider_class:
        mock_provider = Mock()
        mock_cash_df = pd.DataFrame([{"债券现货": "国债", "托管只数": 193}])
        mock_deal_df = pd.DataFrame([{"债券类型": "记账式国债", "当日成交笔数": 3685}])
        
        mock_provider.get_cash_summary = AsyncMock(return_value=mock_cash_df)
        mock_provider.get_deal_summary = AsyncMock(return_value=mock_deal_df)
        mock_provider_class.return_value = mock_provider
        
        with patch('app.worker.bonds_sync_service.get_mongo_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            with patch('app.worker.bonds_sync_service.BondDataService') as mock_service_class:
                mock_service = Mock()
                mock_service.ensure_indexes = AsyncMock()
                mock_service_class.return_value = mock_service
                
                # 执行同步
                sync_service = BondSyncService()
                result = await sync_service.sync_market_summary("20210111")
                
                # 验证
                assert result["success"] is True
                assert result["date"] == "20210111"
                assert len(result["results"]) == 2
                
                # 验证两个方法都被调用
                assert mock_provider.get_cash_summary.called
                assert mock_provider.get_deal_summary.called
    
    print("✅ 测试通过：市场概览同步成功")


@pytest.mark.asyncio
async def test_sync_market_summary_default_date():
    """测试市场概览使用默认日期"""
    from app.worker.bonds_sync_service import BondSyncService
    from datetime import datetime
    
    # Mock Provider
    with patch('app.worker.bonds_sync_service.AKShareBondProvider') as mock_provider_class:
        mock_provider = Mock()
        mock_provider.get_cash_summary = AsyncMock(return_value=pd.DataFrame())
        mock_provider.get_deal_summary = AsyncMock(return_value=pd.DataFrame())
        mock_provider_class.return_value = mock_provider
        
        with patch('app.worker.bonds_sync_service.get_mongo_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            with patch('app.worker.bonds_sync_service.BondDataService') as mock_service_class:
                mock_service = Mock()
                mock_service.ensure_indexes = AsyncMock()
                mock_service_class.return_value = mock_service
                
                # 执行同步（不指定日期）
                sync_service = BondSyncService()
                result = await sync_service.sync_market_summary()
                
                # 验证使用了今天的日期
                today = datetime.now().strftime("%Y%m%d")
                assert result["date"] == today
    
    print("✅ 测试通过：市场概览默认日期")


@pytest.mark.asyncio
async def test_sync_large_dataset():
    """测试同步大数据集"""
    from app.worker.bonds_sync_service import BondSyncService
    
    # Mock返回大数据集（500条）
    with patch('app.worker.bonds_sync_service.AKShareBondProvider') as mock_provider_class:
        mock_provider = Mock()
        # 创建500条测试数据
        large_df = pd.DataFrame([
            {
                "转债代码": f"11{i:04d}",
                "转债名称": f"转债{i}",
                "转债最新价": 100.0 + i * 0.1
            }
            for i in range(500)
        ])
        mock_provider.get_cov_comparison = AsyncMock(return_value=large_df)
        mock_provider_class.return_value = mock_provider
        
        with patch('app.worker.bonds_sync_service.get_mongo_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            with patch('app.worker.bonds_sync_service.BondDataService') as mock_service_class:
                mock_service = Mock()
                mock_service.ensure_indexes = AsyncMock()
                mock_service.save_cov_comparison = AsyncMock(return_value=500)
                mock_service_class.return_value = mock_service
                
                # 执行同步
                sync_service = BondSyncService()
                result = await sync_service.sync_cov_comparison()
                
                # 验证
                assert result["success"] is True
                assert result["saved"] == 500
                assert result["rows"] == 500
    
    print("✅ 测试通过：同步大数据集")


@pytest.mark.asyncio
async def test_concurrent_sync_tasks():
    """测试并发同步任务"""
    from app.worker.bonds_sync_service import BondSyncService
    import asyncio
    
    # Mock Provider
    with patch('app.worker.bonds_sync_service.AKShareBondProvider') as mock_provider_class:
        mock_provider = Mock()
        mock_provider.get_cov_comparison = AsyncMock(return_value=pd.DataFrame([
            {"转债代码": "113682", "转债名称": "益丰转债"}
        ]))
        mock_provider.get_spot_deal = AsyncMock(return_value=pd.DataFrame([
            {"债券简称": "23附息国债26"}
        ]))
        mock_provider_class.return_value = mock_provider
        
        with patch('app.worker.bonds_sync_service.get_mongo_db') as mock_get_db:
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            
            with patch('app.worker.bonds_sync_service.BondDataService') as mock_service_class:
                mock_service = Mock()
                mock_service.ensure_indexes = AsyncMock()
                mock_service.save_cov_comparison = AsyncMock(return_value=1)
                mock_service.save_spot_deals = AsyncMock(return_value=1)
                mock_service_class.return_value = mock_service
                
                # 并发执行多个同步任务
                sync_service = BondSyncService()
                tasks = [
                    sync_service.sync_cov_comparison(),
                    sync_service.sync_spot_deals(),
                    sync_service.sync_cov_comparison(),  # 重复任务
                ]
                
                results = await asyncio.gather(*tasks)
                
                # 验证所有任务都成功
                assert all(r["success"] for r in results)
                assert len(results) == 3
    
    print("✅ 测试通过：并发同步任务")


if __name__ == "__main__":
    # 运行所有测试
    pytest.main([__file__, "-v", "-s"])
