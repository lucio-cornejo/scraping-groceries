module.exports = {
  // Implement sleep function similar to Python's time.sleep function
  sleep : async function sleep (numSeconds) {
    return new Promise(r => setTimeout(r, 1000*numSeconds));
  },
  randomFloatInRange : function (minValue, maxValue) {
    return parseFloat(
      (Math.random() * (maxValue - minValue) + minValue)
        // At most, keep two decimals
        .toFixed(2)
    );
  } 
}
