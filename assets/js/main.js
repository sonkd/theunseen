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
      const menu_icon = document.querySelector(".menu-icon");
      const close_icon = document.querySelector(".close-icon");

      this.checked
        ? (area.classList.add("blurry"), close_icon.removeAttribute("hidden"),
        menu_icon.setAttribute("hidden", ""))
        : (area.classList.remove("blurry"), menu_icon.removeAttribute("hidden"),
        close_icon.setAttribute("hidden", ""));
    });
  };

  // Check isReading state
  if (document.getElementById("post")) {
    const reading = document.getElementById("post");
    var currentPos = 0;

    reading.addEventListener("scroll", function () {
      if (reading.scrollTop > currentPos) {
        document.querySelector("#navpost").setAttribute("hidden", "");
        currentPos = reading.scrollTop;
      } else {
        document.querySelector("#navpost").removeAttribute("hidden");
        currentPos = reading.scrollTop;
      }
    });
  };

  //Share popup
  const viewBtn = document.querySelector(".view-modal"),
    popup = document.querySelector(".popup-share"),
    close = popup.querySelector(".share-close"),
    field = popup.querySelector(".share-field"),
    input = field.querySelector("input"),
    copy = field.querySelector("button");
  
  const viewShareIcon = document.querySelector(".view-modal"),
    popup2 = document.querySelector(".popup-share"),
    close2 = popup2.querySelector(".share-close"),
    field2 = popup2.querySelector(".share-field"),
    input2 = field2.querySelector("input"),
    copy2 = field2.querySelector("#share-icon");
  
  viewBtn.onclick = () => {
    popup.classList.toggle("show");
  }
  close.onclick = () => {
    viewBtn.click();
  }

  viewShareIcon.onclick = () => {
    popup.classList.toggle("show");
  }
  close2.onclick = () => {
    viewShareIcon.click();
  }

  copy.onclick = () => {
    input.select(); //select input value
    if (document.execCommand("copy")) { //if the selected text is copied
      field.classList.add("active");
      copy.innerText = "Copied";
      setTimeout(() => {
        window.getSelection().removeAllRanges(); //remove selection from page
        field.classList.remove("active");
        copy.innerText = "Copy";
      }, 3000);
    }
  }

  copy2.onclick = () => {
    input2.select(); //select input value
    if (document.execCommand("copy")) { //if the selected text is copied
      field2.classList.add("active");
      copy2.innerText = "Copied";
      setTimeout(() => {
        window.getSelection().removeAllRanges(); //remove selection from page
        field2.classList.remove("active");
        copy2.innerText = "Copy";
      }, 3000);
    }
  }

})();
