(() => {
  // Theme switch
  const body = document.body;
  const lamp = document.getElementById("mode");

  const toggleTheme = (state) => {
    if (state === "dark") {
      localStorage.setItem("theme", "light");
      body.removeAttribute("data-theme");
    } else if (state === "light") {
      localStorage.setItem("theme", "dark");
      body.setAttribute("data-theme", "dark");
    } else {
      initTheme(state);
    }
  };

  lamp.addEventListener("click", () =>
    toggleTheme(localStorage.getItem("theme"))
  );

  // Blur the content when the menu is open
  if (document.getElementById("menu-trigger")){
    const cbox = document.getElementById("menu-trigger");

    cbox.addEventListener("change", function () {
      const area = document.querySelector(".wrapper");
      this.checked
        ? area.classList.add("blurry")
        : area.classList.remove("blurry");
    });
  };

  // Check isReading state
  const reading = document.getElementById("post");
  var currentPos = 0;

  reading.addEventListener("scroll", function() {
    if (reading.scrollTop > currentPos) {
      document.querySelector("#navpost").setAttribute("hidden", "");
      currentPos = reading.scrollTop;
    } else {
      document.querySelector("#navpost").removeAttribute("hidden");
      currentPos = reading.scrollTop;
    }
  });

})();
