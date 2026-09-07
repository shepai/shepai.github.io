const projects = [

    {
        title: "Modular Neuromorphic Skin",
        link: "dev/modular-skin.html",
        icon: "https://raw.githubusercontent.com/shepai/TacSheet/refs/heads/main/Assets/backrender.png",
        description: "Our designs based on the PressTip for modular connected skin sheets.",
        keywords: ["tactile", "robotics", "sensors", "PressTip"],
        date: "2026-08-15"
    },

    {
        title: "Tactile ball robot",
        link: "dev/ball.html",
        icon: "https://raw.githubusercontent.com/shepai/tactile-ball-robot/refs/heads/main/assets/ball2.png",
        description: "The project to give tactile perception to a versatile ball robot.",
        keywords: ["tactile", "robotics", "sensors"],
        date: "2026-07-20"
    },

    {
        title: "TacTip gym",
        link: "dev/tactip-gym.html",
        icon: "https://raw.githubusercontent.com/shepai/tactip-gym/refs/heads/main/assets/examplearm.png",
        description: "TacTip gym environment with examples of robot bodies, and simply adding the sensor to a chassis.",
        keywords: ["tactile", "robotics", "simulation", "TacTip"],
        date: "2026-06-10"
    },

    {
        title: "Ant World",
        link: "dev/antenv.html",
        icon: "assets/development/ant.jpg",
        description: "A grid based simulator in Python based on scans for a real ant testing site.",
        keywords: ["simulation", "Python", "bio-inspired", "navigation"],
        date: "2026-05-12"
    },

    {
        title: "3D printed tactile dataset",
        link: "dev/3dprintabledataset.html",
        icon: "assets/development/edited_all.png",
        description: "Benchmarking tactile texture classification tasks in a replicatable way.",
        keywords: ["tactile", "machine learning", "dataset", "3D printing"],
        date: "2026-04-18"
    },

    {
        title: "Texture and friction classification",
        link: "dev/textureclassification.html",
        icon: "assets/development/rig.png",
        description: "A comparison between the two types of tactile sensors we have worked on.",
        keywords: ["tactile", "machine learning", "classification", "sensors"],
        date: "2026-03-22"
    },

    {
        title: "Quadruped evolution",
        link: "dev/quadruped.html",
        icon: "assets/development/robot/pybullet.png",
        description: "Project for creating a CAD quadruped from scratch and evolving gait controllers.",
        keywords: ["robotics", "evolution", "genetic algorithms", "simulation"],
        date: "2026-02-15"
    },

    {
        title: "Tactile Biped",
        link: "dev/biped.html",
        icon: "assets/development/robot/robot.jpeg",
        description: "Using the PressTip foot sensor, we were able to gather a dataset of poses and train a model to recognise its 3D orientation based on tactile readings.",
        keywords: ["tactile", "robotics", "machine learning", "PressTip"],
        date: "2026-01-10"
    },

    {
        title: "PressTip multimodal sensor",
        link: "dev/PressTip.html",
        icon: "assets/development/presstip.jpg",
        description: "The construction of the PressTip sensor, an electrical multimodal tactile sensor.",
        keywords: ["tactile", "sensors", "PressTip", "hardware"],
        date: "2025-12-10"
    },

    {
        title: "TacTip construction",
        link: "dev/TacTip.html",
        icon: "assets/development/pro-P3zmVNxw (1).png",
        description: "The TacTip sensor construction and experimentation across various designs.",
        keywords: ["tactile", "sensors", "TacTip", "hardware"],
        date: "2025-11-15"
    },

    {
        title: "GPS Ant robot",
        link: "dev/GPS.html",
        icon: "assets/development/gpsrobot.jpeg",
        description: "This project worked on constructing a large chassis that could be used for outdoor exploration to test ant inspired algorithms. This project was part of a research assistant role.",
        keywords: ["robotics", "bio-inspired", "navigation", "GPS"],
        date: "2025-10-20"
    },

    {
        title: "Bio-Inspired Navigation for Varied Terrain",
        link: "dev/fyp.html",
        icon: "assets/diss/CUTOUT.png",
        description: "This project uses the Wheg chassis developed in previous projects, however investigates aspects of autonomous navigation behaviours for traversing complex terrain.",
        keywords: ["robotics", "bio-inspired", "navigation", "autonomous"],
        date: "2025-09-01"
    },

    {
        title: "Deep learning for autonomous navigation on small robots",
        link: "dev/JRA.html",
        icon: "assets/nanosaur.jpg",
        description: "This project was part of the University of Sussex Junior Research Associate scheme.",
        keywords: ["machine learning", "deep learning", "robotics", "navigation"],
        date: "2025-07-15"
    },

    {
        title: "Genetic algorithm robot walking optimization",
        link: "dev/GeneticAlgorithms.html",
        icon: "assets/biped.jpg",
        description: "Genetic Algorithms use random mutations within a Genotype which is assessed using a fitness function. In this case fitness being the Genotype which walks the best.",
        keywords: ["robotics", "genetic algorithms", "evolution", "optimization"],
        date: "2025-05-20"
    },

    {
        title: "Exploring planetary terrain",
        link: "dev/probe.html",
        icon: "assets/whegged.JPG",
        description: "In this project we explore different hardware options available for space exploration. This started as a tracked rover controlled via a network.",
        keywords: ["robotics", "space", "exploration", "navigation"],
        date: "2025-03-10"
    }

];


// --------------------------------------------------
// SETTINGS
// --------------------------------------------------

const projectsPerPage = 10;

let currentPage = 1;
let selectedKeywords = [];


// --------------------------------------------------
// SORT PROJECTS BY DATE
// Newest first
// --------------------------------------------------

projects.sort((a, b) => new Date(b.date) - new Date(a.date));


// --------------------------------------------------
// CREATE UNIQUE KEYWORD LIST
// --------------------------------------------------

function createKeywordList() {

    const keywordDropdown = document.getElementById("keywordDropdown");

    const allKeywords = [
        ...new Set(
            projects.flatMap(project => project.keywords)
        )
    ];

    allKeywords.sort((a, b) => a.localeCompare(b));

    keywordDropdown.innerHTML = "";

    allKeywords.forEach(keyword => {

        const label = document.createElement("label");
        label.className = "keywordOption";

        const checkbox = document.createElement("input");

        checkbox.type = "checkbox";
        checkbox.value = keyword;

        checkbox.addEventListener("change", function() {

            if (this.checked) {
                selectedKeywords.push(keyword);
            } else {
                selectedKeywords =
                    selectedKeywords.filter(k => k !== keyword);
            }

            currentPage = 1;
            renderProjects();

        });

        label.appendChild(checkbox);
        label.appendChild(
            document.createTextNode(keyword)
        );

        keywordDropdown.appendChild(label);

    });

}


// --------------------------------------------------
// FILTER PROJECTS
// --------------------------------------------------

function getFilteredProjects() {

    if (selectedKeywords.length === 0) {
        return projects;
    }

    return projects.filter(project => {

        // OR filtering:
        // project appears if it contains ANY selected keyword

        return selectedKeywords.some(keyword =>
            project.keywords.includes(keyword)
        );

    });

}


// --------------------------------------------------
// DISPLAY PROJECTS
// --------------------------------------------------

function renderProjects() {

    const projectList =
        document.getElementById("projectList");

    const filteredProjects =
        getFilteredProjects();

    const totalPages =
        Math.ceil(filteredProjects.length / projectsPerPage);

    // Make sure current page still exists
    if (currentPage > totalPages && totalPages > 0) {
        currentPage = totalPages;
    }

    const start =
        (currentPage - 1) * projectsPerPage;

    const end =
        start + projectsPerPage;

    const pageProjects =
        filteredProjects.slice(start, end);


    let html = `
        <table class="projectTable">
    `;


    pageProjects.forEach((project, index) => {

        // Alternate based on the actual position
        // on the current page.
        const imageLeft = index % 2 === 0;


        if (imageLeft) {

            html += `
                <tr>
                    <th>
                        <a href="${project.link}">
                            <img
                                class="imageCircle2 projectImage"
                                src="${project.icon}"
                                alt="${project.title}"
                            >
                        </a>
                    </th>

                    <th>
                        <a
                            class="projectTitle"
                            href="${project.link}"
                        >
                            ${project.title}
                        </a>

                        <p class="textInfo projectDescription">
                            ${project.description}
                        </p>
                    </th>
                </tr>
            `;

        } else {

            html += `
                <tr>
                    <th>
                        <a
                            class="projectTitle"
                            href="${project.link}"
                        >
                            ${project.title}
                        </a>

                        <p class="textInfo projectDescription">
                            ${project.description}
                        </p>
                    </th>

                    <th>
                        <a href="${project.link}">
                            <img
                                class="imageCircle2 projectImage"
                                src="${project.icon}"
                                alt="${project.title}"
                            >
                        </a>
                    </th>
                </tr>
            `;

        }

    });


    html += `</table>`;

    projectList.innerHTML = html;

    renderPagination(totalPages);

}


// --------------------------------------------------
// PAGINATION
// --------------------------------------------------

function renderPagination(totalPages) {

    const pagination =
        document.getElementById("pagination");

    pagination.innerHTML = "";

    if (totalPages <= 1) {
        return;
    }


    // Previous button

    if (currentPage > 1) {

        const previous =
            document.createElement("button");

        previous.textContent = "← Previous";

        previous.onclick = function() {
            currentPage--;
            renderProjects();
            window.scrollTo(0, 0);
        };

        pagination.appendChild(previous);

    }


    // Page numbers

    for (let page = 1; page <= totalPages; page++) {

        const button =
            document.createElement("button");

        button.textContent = page;

        if (page === currentPage) {
            button.classList.add("active");
        }

        button.onclick = function() {

            currentPage = page;

            renderProjects();

            window.scrollTo(0, 0);

        };

        pagination.appendChild(button);

    }


    // Next button

    if (currentPage < totalPages) {

        const next =
            document.createElement("button");

        next.textContent = "Next →";

        next.onclick = function() {

            currentPage++;

            renderProjects();

            window.scrollTo(0, 0);

        };

        pagination.appendChild(next);

    }

}

