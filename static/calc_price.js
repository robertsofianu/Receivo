var purchasePriceInput = document.getElementById("purchasePrice");
var vatRateSelect = document.getElementById("vatRate");
var sellingPriceInput = document.getElementById("sellingPrice");


purchasePriceInput.addEventListener("input", calculateAndSetPlaceholder);
vatRateSelect.addEventListener("change", calculateAndSetPlaceholder);

function calculateAndSetPlaceholder() {
    var purchasePrice = parseFloat(purchasePriceInput.value);
    var vatRate = parseFloat(vatRateSelect.value);

    var sellingPrice = purchasePrice * 1.3 * (1 + vatRate);

    sellingPriceInput.placeholder = "Recomanded: " + sellingPrice.toFixed(2) + "RON";
}
