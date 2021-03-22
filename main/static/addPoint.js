var target = document.querySelectorAll('.number')
          target.forEach(element => {
            element = element.innerHTML
            if (element.length == 3) {
              element.substring(0) + "." + element.substring(1, element.length);
          } else if (element.length == 4) {
              element.substring(0, 1) + "." + element.substring(2, element.length);
          } else if (element.length == 5) {
              element.substring(0, 2) + "." + element.substring(3, element.length);
          } else if (element.length == 6) {
              element.substring(0) + "." + element.substring(1, 3) + "." + element.substring(4, element.length);
          } else if (element.length == 7) {
              element.substring(0, 1) + "." + element.substring(2, 4) + "." + element.substring(5, element.length);
          }
          console.log(element)
          });