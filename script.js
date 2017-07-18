// localStorage functions.
function searchStorage() {
  this.searchStorageLocal = [];

  this.getStorage =() => {
    let GS = JSON.parse(window.localStorage.getItem("stockCodeStorage")) || 0;
    (GS.length > 0) ? this.searchStorageLocal = GS : this.searchStorageLocal = [];
    window.searchStorageLocal = this.searchStorageLocal;
  };

  this.setStorage = (newValue) => {
    let localBool = true;
    if (this.searchStorageLocal.length > 0) {
      $.each(this.searchStorageLocal, (index, value) => {
        if (value.newCode === newValue) {
          localBool = false;
        }
      });
      if (localBool) {
        this.searchStorageLocal.push({newCode: newValue});
      }
    } else {
      this.searchStorageLocal.push({newCode: newValue});
    }
    window.localStorage.removeItem("stockCodeStorage");
    window.localStorage.setItem("stockCodeStorage", JSON.stringify(this.searchStorageLocal));
    this.getStorage();
  }

  this.clearStorage = () => {
    window.localStorage.removeItem("stockCodeStorage");
    this.getStorage();
  };

  this.appendValues = () => {
    if (this.searchStorageLocal.length > 0) {
      $.each(this.searchStorageLocal, (index, value) => {
          let o = new Option(value.newCode, value.newCode);
          $("#previousStocksId").append(o);
      });
      $(".previousStocks").show();
    }
  };
}

// Pull local storage info and setup functions to play with data.
var storage = new searchStorage();
storage.getStorage();
storage.appendValues();

// Ping Finance API and either throw error or create graph object with data.
var getFinanceData = {
  data: function(timeSeries, stockCode) {
    `https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=${stockCode}&interval=${timeSeries}&apikey=03KMUXXHLTRXD7LD`
    return $.getJSON(`https:/\/www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=${stockCode}&interval=${timeSeries}&apikey=03KMUXXHLTRXD7LD`).then((data) => {
      if (data['Error Message'] === undefined){

        storage.setStorage(stockCode);
        storage.getStorage();
        storage.appendValues();
        $(".previousStocks").show();
        this.postResults(data["Time Series ("+ timeSeries +")"]);

      } else {
        this.error(stockCode);
      }
    });
  },
  error: function(code) {
    (code.length === 0) ? code = "No Code" : code = code;
    $("#guide").hide();
    $("#errorMessage").show().text(`Something went wrong. Please check the stock code again. You entered: ${code}`);
  },
  postResults: function(data) {
    let open = [];
    let high = [];
    let low = [];
    let close = [];
    $.each(data, (index, value) => {
      open.push(parseFloat(value['1. open']));
      high.push(parseFloat(value['2. high']));
      low.push(parseFloat(value['3. low']));
      close.push(parseFloat(value['4. close']));
    });

    let graphData = {
      series: [open,high,low,close]
    }
    new Chartist.Line("#chart", graphData, {
      axisX: {
        showGrid: false,
      }, plugins: [
        Chartist.plugins.legend({
          legendNames: ["  Open","  High","  Low","  Close"]
        })
      ],
      showLine: true,
      showPoint: false,
      width: 800,
      height: 400,
      lineSmooth: true
    });
    $(".chart").show();

    return;

  }
}


// listen for clear button and clear storage and history.
document.getElementById("clearHistory").addEventListener("click", function(){
    storage.clearStorage();
    $(".previousStocks").hide();
});

// take data from form and send to API.
document.getElementById("submit").addEventListener("click", (e) => {
  $("#errorMessage").hide();
  $("#guide").show();
  e.preventDefault();

  // "Enter Stock Below" value.
  let selectStockID = document.getElementById("enterStockInput").value.toString().toUpperCase();

  // "Stock History" value. Takes either the user-selected value, or defaults to None.
  selectOldID = document.getElementById("previousStocksId");
  selectOldIDValue = selectOldID[selectOldID.selectedIndex].text.toString().toUpperCase();

  // "Time Interval" value.
  let timeInterval = document.getElementById("timeIntervalSelect").options;
  let selectedTime = timeInterval[timeInterval.selectedIndex].text;
  let returnedData;

  // If a user selects a value from history use it, if not use typed value.
  if (selectOldIDValue === "NONE") {
    returnedData = getFinanceData.data(selectedTime, selectStockID);
  } else {
    returnedData = getFinanceData.data(selectedTime, selectOldIDValue);
  }
});
