<template>
  <main class="container mt-5">
    <form v-on:submit="onSubmit">
      <div class="form-row">
        <div class="form-group col-md-3">
          <label for="inputProduct">Product</label>
          <select
            id="inputProduct"
            class="form-control"
            v-model="product"
            v-on:change="getQuote"
            required
          >
            <option v-for="product in productsList" :key="product">
              {{
              product
              }}
            </option>
          </select>
        </div>
        <div class="form-group col-md-3">
          <label for="inputPrice">Current Price</label>
          <input
            type="number"
            class="form-control"
            id="inputPrice"
            v-model="currentPrice"
            required
            readonly
          />
        </div>
        <div class="form-group col-md-3">
          <label for="inputPrice">Open Price</label>
          <input type="number" class="form-control" id="inputPrice" v-model="price" required />
        </div>
        <div class="form-group col-md-3">
          <label for="inputSize">Trade Size</label>
          <input type="float" class="form-control" id="inputSize" v-model="size" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group col-md-2">
          <label for="inputStrategy">Strategy</label>
          <select id="inputStrategy" class="form-control" v-model="strategy" required>
            <option>GRID</option>
            <option>DCA</option>
          </select>
        </div>
        <div class="form-group col-md-2">
          <label for="inputSide">Side</label>
          <select id="inputSide" class="form-control" v-model="side" required>
            <option>buy</option>
            <option>sell</option>
          </select>
        </div>
        <div class="form-group col-md-2">
          <label for="inputTrades">Number Of Trades</label>
          <input type="number" class="form-control" id="inputTrades" v-model="trades" required />
        </div>
        <div class="form-group col-md-3">
          <label for="inputProfit">Profit Per Trade In Amount</label>
          <input type="number" class="form-control" id="inputProfit" v-model="profit" required />
        </div>
        <div class="form-group col-md-3">
          <label for="inputDiff">Average UP/DOWN In Amount</label>
          <input type="number" class="form-control" id="inputDiff" v-model="diff" required />
        </div>
      </div>
      <div class="row justify-content-md-center mt-2">
        <button type="submit" class="btn btn-primary">Submit</button>
      </div>
    </form>
    <loading :active.sync="isLoading" :is-full-page="fullPage" loader="dots" color="blue"></loading>
    <div class="row justify-content-md-center mt-2">
      <label
        v-if="errorText.length > 0"
        for="errorText"
        class="primary"
        style="color: red"
      >Error from api: {{ errorText }}</label>
    </div>
    <div class="row justify-content-md-center mt-2">
      <label
        v-if="ordersList.length > 0"
        for="ordersListText"
        class="primary"
      >Submitted below orders</label>
    </div>
    <table v-if="ordersList.length > 0" class="table table-bordered mt-2">
      <thead>
        <tr>
          <th scope="col">product</th>
          <th scope="col">orderId</th>
          <th scope="col">openPrice</th>
          <th scope="col">closePrice</th>
          <th scope="col">side</th>
          <th scope="col">size</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in ordersList" :key="order.id">
          <td>{{ order.product_id }}</td>
          <td>{{ order.order_id }}</td>
          <td>{{ order.open_price }}</td>
          <td>{{ order.close_price }}</td>
          <td>{{ order.side }}</td>
          <td>{{ order.size }}</td>
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
  components: {
    Loading
  },
  name: "trade",
  data() {
    return {
      loading: false,
      productsList: [],
      exchangeName: null,
      ordersList: [],
      currentPrice: null,
      exchange: null,
      product: null,
      price: null,
      size: null,
      trades: null,
      profit: null,
      side: null,
      diff: null,
      strategy: null,
      errorText: "",
      isLoading: false
    };
  },
  mounted: async function() {
    this.getProducts();
  },
  methods: {
    getProducts: async function() {
      this.loading = true;
      this.productsList = [];
      axios
        .get("http://localhost:8080/products")
        .then(response => {
          console.log(response);
          for (let index = 0; index < response.data.length; index++) {
            this.productsList.push(response.data[index]);
          }
          this.loading = false;
        })
        .catch(error => {
          console.log("error:", error.response.data.message);
          this.errorText = error.response.data.message;
        });
    },
    getQuote: async function(event) {
      const data = JSON.stringify({
        symbol: event.target.value
      });
      console.log(data);
      axios
        .post("http://localhost:8080/quote", data)
        .then(response => {
          console.log(response);
          this.currentPrice = response.data.last;
        })
        .catch(error => {
          console.log("error:", error.response.data.message);
          this.errorText = error.response.data.message;
        });
    },
    onSubmit: async function(e) {
      console.log(e);
      e.preventDefault();
      const data = JSON.stringify({
        symbol: this.product,
        price: this.price,
        side: this.side,
        count: this.trades,
        profit: this.profit,
        size: this.size,
        diff: this.diff,
        strategy: this.strategy
      });
      console.log(data);
      this.isLoading = true;
      this.ordersList = [];
      axios
        .post("http://localhost:8080/order", data)
        .then(response => {
          console.log(response);
          this.ordersList = response.data;
          this.isLoading = false;
        })
        .catch(error => {
          console.log("error:", error.response.data.message);
          this.errorText = error.response.data.message;
          this.ordersList = [];
        });
    }
  }
};
</script>

<style>
</style>
