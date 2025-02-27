let IsOpen = false;

/* function to create observer for fade in animations */
function createObserver(className, Delay) {
    const elements = document.querySelectorAll(className);
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('active');
                    observer.unobserve(entry.target);
                }, Delay);
            }
        });
    }, { threshold: 0.1 });

    elements.forEach(element => {
        observer.observe(element);
    });
}

/*function to check viewport size for responsive page */
function checkViewport() {
    const width = window.innerWidth;
    const LeftHalf = document.querySelector('.LeftHalf');

    // Remove all classes from LeftHalf
    if (LeftHalf) {
        console.log('LeftHalf element found');
        LeftHalf.classList.remove('mobile', 'desktop');
    
        // Add class based on width
        if (width <= 767 && IsOpen == true) {
            LeftHalf.classList.add('mobile');
            console.log('Added mobile class');
        } else if (width >= 1024 && IsOpen == true) {
            LeftHalf.classList.add('desktop');
            console.log('Added desktop class');
        } else if (width >= 768 && width <= 1023 && IsOpen == true) {
            LeftHalf.classList.add('tablet');
            console.log('Added tablet class');
        }
    } else {
        console.log('LeftHalf element not found');
    }
}

document.addEventListener('DOMContentLoaded',() => {
    document.querySelectorAll('.animatedStartY').forEach((element, index) => {
        setTimeout(() => {
            element.classList.add('active');
        }, index * 200);
    });

    createObserver('.animatedBotY', 200);
    createObserver('.animatedRightX', 200);
    createObserver('.animatedLeftX', 200);

    // Check viewport size on page load
    checkViewport();

    // Check viewport size on window resize
    window.addEventListener('resize', checkViewport);
});


/* code for the open invitation button */ 
const pages = ['Page2', 'Page3', 'Page4', 'Page5', 'Page6', 'Page7'];

function scrollToContent() {
    IsOpen = true;
    checkViewport();
    pages.forEach(page => {
        document.getElementById(page).style.display = 'flex';
    });
    document.getElementById('Page2').scrollIntoView({ behavior: 'smooth' });
}