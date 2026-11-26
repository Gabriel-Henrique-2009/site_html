import { defineStore } from 'pinia'

export const useItemStore = defineStore('items', {
  state: () => ({
    items: [
      {
        id: 1,
        name: 'Samsung S25 Ultra',
        description: 'foto do samsung s25 ultra'
      },
      {
        id: 2,
        name: 'iPhone 17 Pro Max',
        description: 'foto do iphone 17 pro max'
      },
      {
        id: 3,
        name: 'iPhone 12',
        description: 'foto do iphone 12 acho que nem tem esse pqp'
      }
    ]
  })
})