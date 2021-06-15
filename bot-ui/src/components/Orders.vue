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
    <loading :active.sync="isLoading" :is-full-page="fullPage" loader="dots" color="blue"></loading>

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
              :disabled="submitButtonDisabled"
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
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";
export default {
  name: "orders",
  components: {
    Loading
  },
  data() {
    return {
      ordersList: [],
      exchangesList: [],
      exchange: null,
      errorText: "",
      connection: null,
      submitButtonDisabled: false,
      cancelSpinner: false,
      isLoading: false,
      fullPage: true
    };
  },
  mounted: async function() {
    this.getOrders();
  },
  methods: {
    getOrders: async function() {
      this.isLoading = false;
      axios
        .get("http://localhost:8080/orders")
        .then(response => {
          console.log(response);
          this.ordersList = response.data;
          this.submitButtonDisabled = false;
        })
        .catch(error => {
          console.log("error:", error.response.data.message);
          this.errorText = error.response.data.message;
          this.submitButtonDisabled = false;
        });
    },
    cancelOrder: async function(orderId, idType) {
      this.isLoading = true;
      console.log("cancelSpinner status:", this.cancelSpinner);
      console.log("orderId:", orderId);
      console.log("idType:", idType);
      this.submitButtonDisabled = true;
      axios
        .delete(`http://localhost:8080/order/${orderId}/${idType}`)
        .then(response => {
          console.log(response);
          this.getOrders();
        })
        .catch(error => {
          console.log("error:", error.response.data.message);
          this.errorText = error.response.data.message;
          this.submitButtonDisabled = false;
        });
    }
  }
};
</script>

<style></style>
