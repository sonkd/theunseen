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
  const cbox = document.getElementById("menu-trigger");
  if (cbox) {
    cbox.addEventListener("change", function () {
      const area = document.querySelector(".wrapper");
      const menu_icon = document.querySelector(".menu-icon");
      const close_icon = document.querySelector(".close-icon");

      this.checked
        ? (area.classList.add("blurry"), close_icon.removeAttribute("hidden"),
          menu_icon.setAttribute("hidden", ""))
        : (area.classList.remove("blurry"), menu_icon.removeAttribute("hidden"),
          close_icon.setAttribute("hidden", ""));
    });
  };
  
  $('#modal-container').click(function(){
    $(this).addClass('out');
    $('body').removeClass('modal-active');
  });


  // Check isReading state
  let prevScrollTop = window.scrollY || document.documentElement.scrollTop;
  let prevScrollDirection = '';

  window.addEventListener('scroll', function () {
    const st = window.scrollY || document.documentElement.scrollTop;
    if (st > prevScrollTop && prevScrollDirection !== 'down') {
      // downscroll code here
      document.querySelector("#navpost").setAttribute("hidden", "");
      prevScrollDirection = 'down';
    } else if (st < prevScrollTop && prevScrollDirection !== 'up') {
      // upscroll code
      document.querySelector("#navpost").removeAttribute("hidden");
      prevScrollDirection = 'up';
    }
    prevScrollTop = st <= 0 ? 0 : st; // for Mobile or negative scrolling
  }, false);
})();