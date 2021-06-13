import Vue from 'vue';
import Router from 'vue-router';
import Orders from '@/components/Orders';
import Trade from '@/components/Trade';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/orders',
            name: 'orders',
            component: Orders
        }, {
            path: '/trade',
            name: 'trade',
            component: Trade
        }
    ]
});