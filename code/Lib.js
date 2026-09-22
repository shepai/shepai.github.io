const projects = [
    {
        title:"EasyLabel",
        description:"Simple labeller for dataset making",
        image:"https://github.com/shepai/EasyLabel/raw/main/Example%20assets/image.png",
        link:"https://github.com/shepai/EasyLabel"
    },
    {
        title: "OpenEduBot",
        description: "Tools for MicroPython educational robots for teaching in schools.",
        image: "assets/openEdu.jpg",
        link: "https://github.com/shepai/OpenEduBot/"
    },

    {
        title: "CircuitPython Machine Learning Library",
        description: "Tools for neural network support on embedded CircuitPython devices.",
        image: "assets/tutorials/46090.jpg",
        link: "https://github.com/shepai/Circuit-Python-ML"
    },

    {
        title: "TacTip Gym",
        description: "Gym environment for attaching soft-bodied TacTip simulations.",
        image: "https://raw.githubusercontent.com/shepai/tactip-gym/refs/heads/main/assets/examplearm.png",
        link: "dev/tactip-gym.html"
    },

    {
        title: "Ball Gym",
        description: "An environment for the tactile ball chassis we developed.",
        image: "https://raw.githubusercontent.com/shepai/tactile-ball-robot/refs/heads/main/assets/ball2.png",
        link: "dev/ball.html"
    },

    {
        title: "Robot Feet Library",
        description: "Library for reading PressTip and TacTip sensors.",
        image: "assets/development/presstip.jpg",
        link: "https://github.com/shepai/Robot_foot"
    },

    {
        title: "AI Debugger Gaslight",
        description: "A 'fun' program where trying to kill your code results in an LLM trying to reason to live.",
        image: "assets/face2.png",
        link: "https://github.com/shepai/emotional-blackmail-error-correction"
    },

    {
        title: "Python Chatbot Library",
        description: "An old project (pre-LLM) which takes an array of inputs and processes them in a network of files.",
        image: "assets/SHEPpython2.png",
        link: "library.html"
    },

    {
        title: "Python AI Library",
        description: "A self-learning through conversation bot (pre-LLM).",
        image: "assets/SHEPpython.png",
        link: "AIlib.html"
    }
];

function createProject(project) {

    const item = document.createElement("div");
    item.className = "projects-item";

    const link = document.createElement("a");
    link.href = project.link;

    const image = document.createElement("img");
    image.className = "projects-image";
    image.src = project.image;
    image.alt = project.title;

    const overlay = document.createElement("div");
    overlay.className = "projects-overlay";

    const title = document.createElement("h3");
    title.textContent = project.title;

    const description = document.createElement("p");
    description.textContent = project.description;

    overlay.appendChild(title);
    overlay.appendChild(description);

    link.appendChild(image);
    link.appendChild(overlay);

    item.appendChild(link);

    return item;
}

function arrangeCircle(circle) {

    const items = circle.querySelectorAll(".projects-item");

    const count = items.length;

    const radius = 220;

    const angleStep = (2 * Math.PI) / count;

    items.forEach((item, index) => {

        const angle = index * angleStep - Math.PI / 2;

        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        item.style.left = `${x}px`;
        item.style.top = `${y}px`;

    });
}
function arrangeCircle(circle) {

    const items = circle.querySelectorAll(".projects-item");

    const count = items.length;

    const itemSize = 250;

    const screenWidth = window.innerWidth;

    const radius = Math.min(
        220,
        (screenWidth - itemSize) / 2
    );

    const angleStep = (2 * Math.PI) / count;

    items.forEach((item, index) => {

        const angle =
            index * angleStep - Math.PI / 2;

        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        item.style.left =
            `calc(50% + ${x}px)`;

        item.style.top =
            `calc(50% + ${y}px)`;
    });
}
const display = document.getElementById("projects-display");
const previousButton = document.getElementById("projects-prev");
const nextButton = document.getElementById("projects-next");
const pageInfo = document.getElementById("projects-page-info");

let currentPage = 0;
let projectsPerPage = 8;


/* --------------------------------
   Decide how many projects to show
   -------------------------------- */
function isMobile() {
    return window.innerWidth < 600;
}
function calculateProjectsPerPage() {

    const width = window.innerWidth;

    if (width < 600) {
        // Phone
        return 4;
    }

    if (width < 900) {
        // Small tablet
        return 6;
    }

    // Desktop
    return 8;
}

function displayProjects() {

    display.innerHTML = "";

    projectsPerPage = calculateProjectsPerPage();

    const start = currentPage * projectsPerPage;

    const end = Math.min(
        start + projectsPerPage,
        projects.length
    );

    const visibleProjects = projects.slice(start, end);

    const circle = document.createElement("div");

    if (isMobile()) {
        circle.className = "projects-mobile";
    } else {
        circle.className = "projects-circle";
    }

    visibleProjects.forEach((project) => {

        const item = createProject(project);

        circle.appendChild(item);

    });

    display.appendChild(circle);

    if (isMobile()) {
        arrangeMobile(circle);
    } else {
        arrangeCircle(circle);
    }

    updateNavigation();
}

function displayProjects() {

    display.innerHTML = "";

    projectsPerPage = calculateProjectsPerPage();

    const start = currentPage * projectsPerPage;

    const end = Math.min(
        start + projectsPerPage,
        projects.length
    );

    const visibleProjects = projects.slice(start, end);

    const circle = document.createElement("div");

    if (isMobile()) {
        circle.className = "projects-mobile";
    } else {
        circle.className = "projects-circle";
    }

    visibleProjects.forEach((project) => {

        const item = createProject(project);

        circle.appendChild(item);

    });

    display.appendChild(circle);

    if (isMobile()) {
        arrangeMobile(circle);
    } else {
        arrangeCircle(circle);
    }

    updateNavigation();
}

function arrangeCircle(circle) {

    const items =
        circle.querySelectorAll(".projects-item");

    const count = items.length;

    /*
     * Calculate how large the circles can be
     * based on the available screen width.
     */

    const screenWidth = window.innerWidth;

    const itemSize = 250;

    const maximumRadius = 360;

    const availableRadius =
        (screenWidth - itemSize) / 2;

    const radius = Math.min(
        maximumRadius,
        availableRadius
    );

    const angleStep =
        (2 * Math.PI) / count;

    items.forEach((item, index) => {

        const angle =
            index * angleStep - Math.PI / 2;

        const x =
            Math.cos(angle) * radius;

        const y =
            Math.sin(angle) * radius;

        item.style.left =
            `calc(50% + ${x}px)`;

        item.style.top =
            `calc(50% + ${y}px)`;

    });
}

function updateNavigation() {

    const totalPages =
        Math.ceil(projects.length / projectsPerPage);

    previousButton.disabled =
        currentPage === 0;

    nextButton.disabled =
        currentPage >= totalPages - 1;

    pageInfo.textContent =
        `${currentPage + 1} / ${totalPages}`;

    /*
     * Hide navigation if everything fits
     * on one page.
     */

    if (totalPages <= 1) {

        previousButton.style.display = "none";
        nextButton.style.display = "none";
        pageInfo.style.display = "none";

    } else {

        previousButton.style.display = "";
        nextButton.style.display = "";
        pageInfo.style.display = "";

    }
}
nextButton.addEventListener("click", () => {

    const totalPages =
        Math.ceil(projects.length / projectsPerPage);

    if (currentPage < totalPages - 1) {
        currentPage++;
        displayProjects();
    }

});


previousButton.addEventListener("click", () => {

    if (currentPage > 0) {
        currentPage--;
        displayProjects();
    }

});


/* Recalculate layout when window is resized */

window.addEventListener("resize", () => {
    displayProjects();
});


/* =================================
   INITIALISE PROJECTS
   ================================= */

displayProjects();