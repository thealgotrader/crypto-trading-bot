<template>
  <main class="container mt-5">
    <div class="row justify-content-md-center mt-2">
      <label
        v-if="errorText.length > 0"
        for="errorText"
        class="primary"
        style="color: red"
      >Error from api: {{ errorText }}</label>
    </div>
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
import axios from "axios";
export default {
  name: "orders",
  data() {
    return {
      ordersList: [],
      exchangesList: [],
      exchange: null,
      errorText: "",
      connection: null
    };
  },
  mounted: async function() {
    this.getOrders();
  },
  methods: {
    getOrders: async function() {
      axios
        .get("http://localhost:8080/orders")
        .then(response => {
          console.log(response);
          this.ordersList = response.data;
        })
        .catch(error => {
          console.log("error:", error.response.data.message);
          this.errorText = error.response.data.message;
        });
    },
    cancelOrder: async function(orderId, idType) {
      console.log("orderId:", orderId);
      console.log("idType:", idType);
      axios
        .delete(`http://localhost:8080/order/${orderId}/${idType}`)
        .then(response => {
          console.log(response);
          this.getOrders();
        })
        .catch(error => {
          console.log("error:", error.response.data.message);
          this.errorText = error.response.data.message;
        });
    }
  }
};
</script>

<style></style>
