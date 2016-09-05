function toggleDiff(event) {
  'use strict';

  /* requires element.classList */
  var i, sha, elements, elem;

  sha = event.target.id;
  elements = document.getElementsByClassName('contrib-vcs-diff');
  for (i = 0; i < elements.length; i += 1) {
    elem = elements[i];
    if (elem.id === sha) {
      elem.classList.toggle('toggle-open');
      elem.classList.toggle('toggle-close');
      break;
    }
  }
}

function addToggleDiffEvent() {
  'use strict';

  var i, elements = document.getElementsByClassName('contrib-vcs-message');
  for (i = 0; i < elements.length; i += 1) {
    elements[i].addEventListener('click', toggleDiff, false);
  }
}

$(document).ready(function () {
  'use strict';

  addToggleDiffEvent();
});
