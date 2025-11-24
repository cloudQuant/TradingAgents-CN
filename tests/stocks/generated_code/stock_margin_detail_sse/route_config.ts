{
  path: '/stocks/collections/stock_margin_detail_sse',
  name: 'StockMarginDetailSse',
  component: () => import('@/views/Stocks/Collections/StockMarginDetailSse.vue'),
  meta: { title: '融资融券明细', requiresAuth: true }
},