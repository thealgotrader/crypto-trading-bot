<template>
  <main class="container mt-5">
    <form>
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
        <button type="submit" v-on:click="onSubmit" class="btn btn-primary">Submit</button>
      </div>
    </form>
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
export default {
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
      strategy: null
    };
  },
  mounted: async function() {
    this.getProducts();
  },
  methods: {
    getProducts: async function() {
      this.loading = true;
      this.productsList = [];
      const response = await fetch(`http://localhost:8080/products`, {
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

      for (let index = 0; index < response.length; index++) {
        this.productsList.push(response[index]);
      }
      this.loading = false;
    },
    getQuote: async function(event) {
      const data = {
        symbol: event.target.value
      };
      console.log(data);
      const response = await fetch(`http://localhost:8080/quote`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: new Headers({
          "content-type": "application/json"
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
      console.log(response);
      this.currentPrice = response.last;
    },
    onSubmit: async function() {
      const data = {
        symbol: this.product,
        price: this.price,
        side: this.side,
        count: this.trades,
        profit: this.profit,
        size: this.size,
        diff: this.diff,
        strategy: this.strategy
      };
      console.log(data);
      const response = await fetch(`http://localhost:8080/order`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: new Headers({
          "content-type": "application/json"
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
      console.log(response);
      this.ordersList = response;
    }
  }
};
</script>

<style>
</style>
