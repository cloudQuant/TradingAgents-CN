<template>
  <component :is="collectionComponent" v-if="collectionComponent" />
  <div v-else class="loading-container">
    <el-loading :loading="true" text="加载中..." />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, defineAsyncComponent } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const collectionName = computed(() => route.params.collectionName as string)

// 将集合名称转换为 PascalCase 组件名
function toPascalCase(name: string): string {
  return name.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join('')
}

// 动态生成组件映射
const collectionComponents: Record<string, () => Promise<any>> = {}
const collectionNames = [
  'fund_name_em', 'fund_basic_info', 'fund_info_index_em', 'fund_ranking',
  'fund_purchase_status', 'fund_etf_spot_em', 'fund_etf_spot_ths', 'fund_lof_spot_em', 'fund_spot_sina',
  'fund_etf_hist_min_em', 'fund_lof_hist_min_em', 'fund_etf_hist_em', 'fund_lof_hist_em', 'fund_etf_hist_sina',
  'fund_open_fund_daily_em', 'fund_open_fund_info_em', 'fund_money_fund_daily_em', 'fund_money_fund_info_em',
  'fund_etf_fund_daily_em', 'fund_hk_hist_em', 'fund_etf_fund_info_em', 'fund_etf_dividend_sina',
  'fund_fh_em', 'fund_cf_em', 'fund_fh_rank_em', 'fund_open_fund_rank_em', 'fund_exchange_rank_em',
  'fund_money_rank_em', 'fund_hk_rank_em', 'fund_individual_achievement_xq',
  'fund_value_estimation_em', 'fund_individual_analysis_xq', 'fund_individual_profit_probability_xq',
  'fund_individual_detail_hold_xq', 'fund_overview_em', 'fund_fee_em', 'fund_individual_detail_info_xq',
  'fund_portfolio_hold_em', 'fund_portfolio_bond_hold_em', 'fund_portfolio_industry_allocation_em',
  'fund_portfolio_change_em', 'fund_rating_all_em', 'fund_rating_sh_em', 'fund_rating_zs_em', 'fund_rating_ja_em',
  'fund_manager_em', 'fund_new_found_em', 'fund_scale_open_sina', 'fund_scale_close_sina',
  'fund_aum_em', 'fund_aum_trend_em', 'fund_aum_hist_em',
  'reits_realtime_em', 'reits_hist_em', 'fund_report_stock_cninfo', 'fund_report_industry_allocation_cninfo',
  'fund_report_asset_allocation_cninfo', 'fund_scale_change_em', 'fund_hold_structure_em',
  'fund_stock_position_lg', 'fund_balance_position_lg', 'fund_linghuo_position_lg',
  'fund_announcement_dividend_em', 'fund_announcement_report_em', 'fund_announcement_personnel_em'
]

// 为每个集合注册组件
collectionNames.forEach(name => {
  const componentName = toPascalCase(name)
  collectionComponents[name] = () => import(/* @vite-ignore */ `./${componentName}.vue`)
})

const collectionComponent = ref<any>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const name = collectionName.value
    if (!name) {
      ElMessage.error('集合名称不能为空')
      return
    }

    const componentLoader = collectionComponents[name]
    if (componentLoader) {
      collectionComponent.value = defineAsyncComponent(componentLoader)
    } else {
      // 如果没有找到对应的组件，使用通用组件
      ElMessage.warning(`集合 ${name} 的组件尚未创建，使用默认组件`)
      collectionComponent.value = defineAsyncComponent(() => import('./DefaultCollection.vue'))
    }
  } catch (error: any) {
    console.error('加载集合组件失败:', error)
    ElMessage.error(`加载集合组件失败: ${error.message}`)
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
.loading-container {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
