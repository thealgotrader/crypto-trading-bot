<template>
  <main class="container mt-5">
    <table class="table table-bordered">
      <thead>
        <tr>
          <th scope="col">product</th>
          <th scope="col">price</th>
          <th scope="col">side</th>
          <th scope="col">size</th>
          <th scope="col">action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in ordersList" :key="order.id">
          <td>{{ order.product }}</td>
          <td>{{ order.price }}</td>
          <td>{{ order.side }}</td>
          <td>{{ order.size }}</td>
          <td>
            <button
              class="btn btn-warning"
              type="button"
              v-on:click="cancelOrder(order.id, order.id_type)"
            >cancel</button>
          </td>
        </tr>
      </tbody>
    </table>
  </main>
</template>

<script>
export default {
  name: "orders",
  data() {
    return {
      ordersList: [],
      exchangesList: [],
      exchange: null
    };
  },
  mounted: async function() {
    this.getOrders();
  },
  methods: {
    getOrders: async function() {
      const response = await fetch(`http://localhost:8080/orders`, {
        method: "GET"
      })
        .then(response => {
          return response.json();
        })
        .catch(error => {
          // Your error is here!
          console.log(error);
          this.$router.push({ path: "/error" });
        });
      this.ordersList = response;
    },
    cancelOrder: async function(orderId, idType) {
      console.log("orderId:", orderId);
      await fetch(`http://localhost:8080/order/${orderId}/${idType}`, {
        method: "DELETE",
        headers: new Headers({
          "content-type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`
        })
      })
        .then(response => {
          return response.json();
        })
        .catch(error => {
          // Your error is here!
          console.log(error);
          this.$router.push({ path: "/error" });
        });
      this.getOrders();
    }
  }
};
</script>

<style></style>
