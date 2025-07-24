document.addEventListener("DOMContentLoaded", function() {
          // Automatically close the notifications after 5 seconds
          setTimeout(function() {
            const notifications = document.querySelectorAll('.notification');
            notifications.forEach(function(notification) {
              notification.style.display = 'none';
            });
          }, 2000); // 5000 milliseconds (5 seconds)
        });