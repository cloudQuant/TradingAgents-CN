# 重复 Logger 定义修复报告

## 概要

- 扫描文件总数: 321
- 发现重复定义文件数: 98
- 成功修复文件数: 98
- 总共移除重复定义: 108
- 修复失败文件数: 0

## 修复详情

### fix_stock_code_issue.py

- 原有 logger 定义数: 3
  - 第 12 行: `logger = get_logger('default')`
  - 第 106 行: `logger = get_logger("default")`
  - 第 139 行: `logger = get_logger('default')`

### main.py

- 原有 logger 定义数: 2
  - 第 6 行: `logger = get_logger('default')`
  - 第 8 行: `logger = get_logger('default')`

### quick_syntax_check.py

- 原有 logger 定义数: 2
  - 第 16 行: `logger = get_logger('default')`
  - 第 18 行: `logger = get_logger('default')`

### stock_code_validator.py

- 原有 logger 定义数: 2
  - 第 17 行: `logger = get_logger('default')`
  - 第 19 行: `logger = get_logger('default')`

### syntax_checker.py

- 原有 logger 定义数: 2
  - 第 16 行: `logger = get_logger('default')`
  - 第 18 行: `logger = get_logger('default')`

### test_fundamentals_tracking.py

- 原有 logger 定义数: 2
  - 第 25 行: `logger = get_logger("default")`
  - 第 97 行: `logger = get_logger("default")`

### test_simple_tracking.py

- 原有 logger 定义数: 3
  - 第 25 行: `logger = get_logger("default")`
  - 第 75 行: `logger = get_logger("default")`
  - 第 125 行: `logger = get_logger("default")`

### data\scripts\sync_stock_info_to_mongodb.py

- 原有 logger 定义数: 2
  - 第 17 行: `logger = get_logger('scripts')`
  - 第 397 行: `logger = get_logger('scripts')`

### examples\batch_analysis.py

- 原有 logger 定义数: 2
  - 第 14 行: `logger = get_logger('default')`
  - 第 24 行: `logger = get_logger('default')`

### examples\cli_demo.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('cli')`
  - 第 15 行: `logger = get_logger('cli')`

### examples\config_management_demo.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 253 行: `logger = get_logger('default')`

### examples\custom_analysis_demo.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 277 行: `logger = get_logger('default')`

### examples\data_dir_config_demo.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 243 行: `logger = get_logger('default')`

### examples\demo_deepseek_analysis.py

- 原有 logger 定义数: 2
  - 第 14 行: `logger = get_logger('default')`
  - 第 208 行: `logger = get_logger('default')`

### examples\my_stock_analysis.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 123 行: `logger = get_logger('default')`

### examples\simple_analysis_demo.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 202 行: `logger = get_logger('default')`

### examples\stock_list_example.py

- 原有 logger 定义数: 2
  - 第 14 行: `logger = get_logger('default')`
  - 第 16 行: `logger = get_logger('default')`

### examples\stock_query_examples.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 249 行: `logger = get_logger('default')`

### examples\token_tracking_demo.py

- 原有 logger 定义数: 2
  - 第 19 行: `logger = get_logger('default')`
  - 第 33 行: `logger = get_logger('default')`

### examples\tushare_demo.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 258 行: `logger = get_logger('default')`

### examples\dashscope_examples\demo_dashscope.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 124 行: `logger = get_logger('default')`

### examples\dashscope_examples\demo_dashscope_chinese.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 146 行: `logger = get_logger('default')`

### examples\dashscope_examples\demo_dashscope_no_memory.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 115 行: `logger = get_logger('default')`

### examples\dashscope_examples\demo_dashscope_simple.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 111 行: `logger = get_logger('default')`

### examples\openai\demo_openai.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 22 行: `logger = get_logger('default')`

### scripts\analyze_data_calls.py

- 原有 logger 定义数: 2
  - 第 18 行: `logger = get_logger('scripts')`
  - 第 20 行: `logger = get_logger('scripts')`

### scripts\build_docker_with_pdf.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('scripts')`
  - 第 15 行: `logger = get_logger('scripts')`

### scripts\install_pandoc.py

- 原有 logger 定义数: 2
  - 第 15 行: `logger = get_logger('scripts')`
  - 第 37 行: `logger = get_logger('scripts')`

### scripts\install_pdf_tools.py

- 原有 logger 定义数: 2
  - 第 15 行: `logger = get_logger('scripts')`
  - 第 178 行: `logger = get_logger('scripts')`

### scripts\log_analyzer.py

- 原有 logger 定义数: 2
  - 第 18 行: `logger = get_logger('scripts')`
  - 第 20 行: `logger = get_logger('scripts')`

### scripts\migrate_to_unified_logging.py

- 原有 logger 定义数: 2
  - 第 16 行: `logger = get_logger('scripts')`
  - 第 18 行: `logger = get_logger('scripts')`

### scripts\setup-docker.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('scripts')`
  - 第 121 行: `logger = get_logger('scripts')`

### scripts\deployment\create_github_release.py

- 原有 logger 定义数: 2
  - 第 14 行: `logger = get_logger('scripts')`
  - 第 16 行: `logger = get_logger('scripts')`

### scripts\deployment\release_v0.1.2.py

- 原有 logger 定义数: 2
  - 第 14 行: `logger = get_logger('scripts')`
  - 第 16 行: `logger = get_logger('scripts')`

### scripts\deployment\release_v0.1.3.py

- 原有 logger 定义数: 2
  - 第 14 行: `logger = get_logger('scripts')`
  - 第 16 行: `logger = get_logger('scripts')`

### scripts\development\adaptive_cache_manager.py

- 原有 logger 定义数: 2
  - 第 19 行: `logger = get_logger('scripts')`
  - 第 114 行: `logger = get_logger('scripts')`

### scripts\development\download_finnhub_sample_data.py

- 原有 logger 定义数: 2
  - 第 19 行: `logger = get_logger('scripts')`
  - 第 232 行: `logger = get_logger('scripts')`

### scripts\development\fix_streamlit_watcher.py

- 原有 logger 定义数: 2
  - 第 19 行: `logger = get_logger('scripts')`
  - 第 21 行: `logger = get_logger('scripts')`

### scripts\development\organize_scripts.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('scripts')`
  - 第 15 行: `logger = get_logger('scripts')`

### scripts\development\prepare_upstream_contribution.py

- 原有 logger 定义数: 2
  - 第 17 行: `logger = get_logger('scripts')`
  - 第 19 行: `logger = get_logger('scripts')`

### scripts\git\branch_manager.py

- 原有 logger 定义数: 2
  - 第 14 行: `logger = get_logger('scripts')`
  - 第 16 行: `logger = get_logger('scripts')`

### scripts\git\check_branch_overlap.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('scripts')`
  - 第 15 行: `logger = get_logger('scripts')`

### scripts\maintenance\branch_manager.py

- 原有 logger 定义数: 2
  - 第 14 行: `logger = get_logger('scripts')`
  - 第 139 行: `logger = get_logger('scripts')`

### scripts\maintenance\cleanup_cache.py

- 原有 logger 定义数: 2
  - 第 14 行: `logger = get_logger('scripts')`
  - 第 146 行: `logger = get_logger('scripts')`

### scripts\maintenance\finalize_script_organization.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('scripts')`
  - 第 338 行: `logger = get_logger('scripts')`

### scripts\maintenance\organize_root_scripts.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('scripts')`
  - 第 233 行: `logger = get_logger('scripts')`

### scripts\maintenance\sync_upstream.py

- 原有 logger 定义数: 2
  - 第 15 行: `logger = get_logger('scripts')`
  - 第 254 行: `logger = get_logger('scripts')`

### scripts\maintenance\version_manager.py

- 原有 logger 定义数: 2
  - 第 16 行: `logger = get_logger('scripts')`
  - 第 18 行: `logger = get_logger('scripts')`

### scripts\setup\configure_pip_source.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('scripts')`
  - 第 224 行: `logger = get_logger('scripts')`

### scripts\setup\initialize_system.py

- 原有 logger 定义数: 2
  - 第 14 行: `logger = get_logger('scripts')`
  - 第 323 行: `logger = get_logger('scripts')`

### scripts\setup\init_database.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('scripts')`
  - 第 221 行: `logger = get_logger('scripts')`

### scripts\setup\manual_pip_config.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('scripts')`
  - 第 214 行: `logger = get_logger('scripts')`

### scripts\setup\migrate_env_to_config.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('scripts')`
  - 第 172 行: `logger = get_logger('scripts')`

### scripts\setup\setup_databases.py

- 原有 logger 定义数: 2
  - 第 15 行: `logger = get_logger('scripts')`
  - 第 198 行: `logger = get_logger('scripts')`

### scripts\validation\check_dependencies.py

- 原有 logger 定义数: 2
  - 第 14 行: `logger = get_logger('scripts')`
  - 第 135 行: `logger = get_logger('scripts')`

### scripts\validation\check_system_status.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('scripts')`
  - 第 251 行: `logger = get_logger('scripts')`

### scripts\validation\smart_config.py

- 原有 logger 定义数: 2
  - 第 16 行: `logger = get_logger('scripts')`
  - 第 63 行: `logger = get_logger('scripts')`

### scripts\validation\verify_gitignore.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('scripts')`
  - 第 15 行: `logger = get_logger('scripts')`

### tradingagents\agents\utils\agent_utils.py

- 原有 logger 定义数: 3
  - 第 23 行: `logger = get_logger('agents')`
  - 第 24 行: `logger = get_logger("agents.utils")`
  - 第 1133 行: `logger = get_logger('agents')`

### tradingagents\api\stock_api.py

- 原有 logger 定义数: 3
  - 第 15 行: `logger = get_logger('agents')`
  - 第 24 行: `logger = get_logger("default")`
  - 第 29 行: `logger = get_logger('agents')`

### tradingagents\config\config_manager.py

- 原有 logger 定义数: 3
  - 第 20 行: `logger = get_logger('agents')`
  - 第 21 行: `logger = get_logger("config")`
  - 第 455 行: `logger = get_logger('agents')`

### tradingagents\config\mongodb_storage.py

- 原有 logger 定义数: 2
  - 第 15 行: `logger = get_logger('agents')`
  - 第 269 行: `logger = get_logger('agents')`

### tradingagents\dataflows\akshare_utils.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('agents')`
  - 第 240 行: `logger = get_logger('agents')`

### tradingagents\dataflows\cache_manager.py

- 原有 logger 定义数: 2
  - 第 18 行: `logger = get_logger('agents')`
  - 第 97 行: `logger = get_logger('agents')`

### tradingagents\dataflows\data_source_manager.py

- 原有 logger 定义数: 3
  - 第 15 行: `logger = get_logger('agents')`
  - 第 444 行: `logger = get_logger('agents')`
  - 第 445 行: `logger = get_logger("default")`

### tradingagents\dataflows\db_cache_manager.py

- 原有 logger 定义数: 2
  - 第 17 行: `logger = get_logger('agents')`
  - 第 200 行: `logger = get_logger('agents')`

### tradingagents\dataflows\finnhub_utils.py

- 原有 logger 定义数: 2
  - 第 6 行: `logger = get_logger('agents')`
  - 第 8 行: `logger = get_logger('agents')`

### tradingagents\dataflows\googlenews_utils.py

- 原有 logger 定义数: 2
  - 第 11 行: `logger = get_logger('agents')`
  - 第 13 行: `logger = get_logger('agents')`

### tradingagents\dataflows\hk_stock_utils.py

- 原有 logger 定义数: 2
  - 第 15 行: `logger = get_logger('agents')`
  - 第 17 行: `logger = get_logger('agents')`

### tradingagents\dataflows\interface.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('agents')`
  - 第 1594 行: `logger = get_logger('agents')`

### tradingagents\dataflows\optimized_china_data.py

- 原有 logger 定义数: 2
  - 第 17 行: `logger = get_logger('agents')`
  - 第 549 行: `logger = get_logger('agents')`

### tradingagents\dataflows\optimized_us_data.py

- 原有 logger 定义数: 2
  - 第 19 行: `logger = get_logger('agents')`
  - 第 275 行: `logger = get_logger('agents')`

### tradingagents\dataflows\realtime_news_utils.py

- 原有 logger 定义数: 2
  - 第 17 行: `logger = get_logger('agents')`
  - 第 19 行: `logger = get_logger('agents')`

### tradingagents\dataflows\stock_api.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('agents')`
  - 第 93 行: `logger = get_logger('agents')`

### tradingagents\dataflows\stock_data_service.py

- 原有 logger 定义数: 2
  - 第 15 行: `logger = get_logger('agents')`
  - 第 272 行: `logger = get_logger('agents')`

### tradingagents\dataflows\tdx_utils.py

- 原有 logger 定义数: 2
  - 第 15 行: `logger = get_logger('agents')`
  - 第 852 行: `logger = get_logger('agents')`

### tradingagents\dataflows\tushare_utils.py

- 原有 logger 定义数: 3
  - 第 17 行: `logger = get_logger('agents')`
  - 第 22 行: `logger = get_logger("default")`
  - 第 62 行: `logger = get_logger('agents')`

### tradingagents\dataflows\utils.py

- 原有 logger 定义数: 2
  - 第 9 行: `logger = get_logger('agents')`
  - 第 11 行: `logger = get_logger('agents')`

### tradingagents\dataflows\yfin_utils.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('agents')`
  - 第 19 行: `logger = get_logger('agents')`

### tradingagents\dataflows\__init__.py

- 原有 logger 定义数: 2
  - 第 8 行: `logger = get_logger('agents')`
  - 第 29 行: `logger = get_logger('agents')`

### tradingagents\graph\trading_graph.py

- 原有 logger 定义数: 3
  - 第 25 行: `logger = get_logger('agents')`
  - 第 26 行: `logger = get_logger("graph.trading_graph")`
  - 第 111 行: `logger = get_logger('agents')`

### tradingagents\llm_adapters\dashscope_adapter.py

- 原有 logger 定义数: 2
  - 第 22 行: `logger = get_logger('agents')`
  - 第 24 行: `logger = get_logger('agents')`

### tradingagents\llm_adapters\dashscope_openai_adapter.py

- 原有 logger 定义数: 2
  - 第 17 行: `logger = get_logger('agents')`
  - 第 228 行: `logger = get_logger('agents')`

### tradingagents\utils\logging_init.py

- 原有 logger 定义数: 4
  - 第 30 行: `logger = get_logger('tradingagents.init')`
  - 第 59 行: `logger = get_logger(logger_name)`
  - 第 92 行: `logger = get_logger('tradingagents.startup')`
  - 第 118 行: `logger = get_logger('tradingagents.shutdown')`

### tradingagents\utils\logging_manager.py

- 原有 logger 定义数: 2
  - 第 19 行: `logger = get_logger('agents')`
  - 第 21 行: `logger = get_logger('agents')`

### upstream_contribution\batch1_caching\tradingagents\dataflows\cache_manager.py

- 原有 logger 定义数: 2
  - 第 18 行: `logger = get_logger('agents')`
  - 第 97 行: `logger = get_logger('agents')`

### upstream_contribution\batch1_caching\tradingagents\dataflows\optimized_us_data.py

- 原有 logger 定义数: 2
  - 第 19 行: `logger = get_logger('agents')`
  - 第 240 行: `logger = get_logger('agents')`

### upstream_contribution\batch2_error_handling\tradingagents\agents\analysts\fundamentals_analyst.py

- 原有 logger 定义数: 2
  - 第 9 行: `logger = get_logger('agents')`
  - 第 258 行: `logger = get_logger('agents')`

### upstream_contribution\batch2_error_handling\tradingagents\agents\analysts\market_analyst.py

- 原有 logger 定义数: 2
  - 第 9 行: `logger = get_logger('agents')`
  - 第 212 行: `logger = get_logger('agents')`

### upstream_contribution\batch2_error_handling\tradingagents\dataflows\db_cache_manager.py

- 原有 logger 定义数: 2
  - 第 17 行: `logger = get_logger('agents')`
  - 第 200 行: `logger = get_logger('agents')`

### upstream_contribution\batch3_data_sources\tradingagents\dataflows\optimized_us_data.py

- 原有 logger 定义数: 2
  - 第 19 行: `logger = get_logger('agents')`
  - 第 240 行: `logger = get_logger('agents')`

### utils\check_version_consistency.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 15 行: `logger = get_logger('default')`

### utils\cleanup_unnecessary_dirs.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 15 行: `logger = get_logger('default')`

### utils\update_data_source_references.py

- 原有 logger 定义数: 2
  - 第 13 行: `logger = get_logger('default')`
  - 第 15 行: `logger = get_logger('default')`

### web\components\analysis_form.py

- 原有 logger 定义数: 2
  - 第 10 行: `logger = get_logger('web')`
  - 第 12 行: `logger = get_logger('web')`

### web\components\results_display.py

- 原有 logger 定义数: 2
  - 第 16 行: `logger = get_logger('web')`
  - 第 219 行: `logger = get_logger('web')`

### web\utils\docker_pdf_adapter.py

- 原有 logger 定义数: 2
  - 第 14 行: `logger = get_logger('web')`
  - 第 90 行: `logger = get_logger('web')`

### web\utils\report_exporter.py

- 原有 logger 定义数: 2
  - 第 19 行: `logger = get_logger('web')`
  - 第 533 行: `logger = get_logger('web')`
