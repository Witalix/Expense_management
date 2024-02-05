document.addEventListener("DOMContentLoaded", function() {
  updateChart(); // Aktualizacja wykresu przy ładowaniu strony

  // Obsługa zdarzenia zmiany wybranej metody płatności
  document.getElementById('paymentMethodSelect').addEventListener('change', function() {
    updateChart();
  });
});

function updateChart() {
  var selectedMethodId = document.getElementById('paymentMethodSelect').value;

  fetch(`/get_payment_methods_categories/?method_id=${selectedMethodId}`)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      var ctx = document.getElementById('myChart').getContext('2d');
      var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.labels,
          datasets: [{
            label: 'Wartości kategorii',
            data: data.values,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    });
}