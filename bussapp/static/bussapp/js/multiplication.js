
document.addEventListener("DOMContentLoaded", () => {
    const fuelLtrInput = document.querySelector('[name="fuel_ltr"]');
    const fuelRateInput = document.querySelector('[name="fuel_rate_per_ltr"]');
    const totalFuelPriceInput = document.querySelector('[name="total_fuel_price"]');

    function calculateTotalFuelPrice() {
        const fuelLtr = parseFloat(fuelLtrInput.value) || 0;
        const fuelRate = parseFloat(fuelRateInput.value) || 0;
        totalFuelPriceInput.value = (fuelLtr * fuelRate).toFixed(2);
    }

    fuelLtrInput.addEventListener('input', calculateTotalFuelPrice);
    fuelRateInput.addEventListener('input', calculateTotalFuelPrice);
});
