    function createBubble() {
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
  
        const randomSize = Math.floor(Math.random() * 30) + 10 + 'px';
        bubble.style.width = randomSize;
        bubble.style.height = randomSize;
  
        const randomPosition = Math.floor(Math.random() * 100) + '%';
        bubble.style.left = randomPosition;
  
        const randomDelay = Math.random() * 10 + 's';
        bubble.style.animationDelay = randomDelay;
  
        document.querySelector('.bubbles').appendChild(bubble);
  
        // Remove bubble from DOM after animation completes
        bubble.addEventListener('animationend', function() {
          bubble.remove();
        });
      }
  
      // Create bubbles at intervals
      setInterval(createBubble, 500);