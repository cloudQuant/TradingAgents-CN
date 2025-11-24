{
  path: '/stocks/collections/stock_margin_sse',
  name: 'StockMarginSse',
  component: () => import('@/views/Stocks/Collections/StockMarginSse.vue'),
  meta: { title: '融资融券汇总', requiresAuth: true }
},