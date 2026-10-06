// publications.js
// PART 1: your data. Edit this to add publications or events.
//   - Keep a comma between entries, and no comma after the last one in a list.
// PART 2 (further down): the code that builds the page. No need to edit it.

/* ================= PART 1: DATA ================= */

const SITE_DATA = {
  "publications": [
    {
      "year": 2026,
      "type": "PhD Thesis",
      "title": "Get a grip: evaluating tactile sensing technologies for adaptive robotic locomotion",
      "authors": "Shepherd D.",
      "venue": "University of Sussex",
      "links": [
        {
          "label": "Full text",
          "url": "https://sussex.figshare.com/articles/thesis/Get_a_grip_evaluating_tactile_sensing_technologies_for_adaptive_robotic_locomotion/33456109?file=68276902"
        },
        {
          "label": "Handle",
          "url": "https://hdl.handle.net/10779/uos.33456109.v1"
        }
      ]
    },
    {
      "year": 2026,
      "type": "Preprint",
      "title": "A 3D-Printable Dataset for Fair Testing and Comparisons of Tactile Sensors",
      "authors": "Shepherd D., Herzig N., Husbands P., et al.",
      "venue": "arXiv (Cornell University)",
      "links": [
        {
          "label": "arXiv",
          "url": "https://arxiv.org/abs/2606.25886"
        }
      ]
    },
    {
      "year": 2025,
      "type": "Dataset",
      "title": "3D Printable Tactile Dataset",
      "authors": "Shepherd D., Husbands P., Herzig N., et al.",
      "venue": "University of Sussex",
      "doi": "10.25377/sussex.30256453"
    },
    {
      "year": 2025,
      "type": "Dataset",
      "title": "Electrical Tactile Dataset (Piezoelectric & Accelerometer) for Textures",
      "authors": "Shepherd D., Philippides A., Husbands P., et al.",
      "venue": "University of Sussex",
      "doi": "10.25377/sussex.28033589.v1"
    },
    {
      "year": 2025,
      "type": "Dataset",
      "title": "Optical Tactile (TacTip) Dataset for Texture Classification",
      "authors": "Shepherd D., Husbands P., Johnson C., et al.",
      "venue": "University of Sussex",
      "doi": "10.25377/sussex.26935696.v1"
    },
    {
      "year": 2025,
      "type": "Journal Article",
      "title": "Texture and friction classification: optical TacTip vs. vibrational piezoelectric and accelerometer tactile sensors",
      "authors": "Shepherd D., Husbands P., Philippides A., et al.",
      "venue": "Sensors, MDPI",
      "doi": "10.3390/s25164971"
    },
    {
      "year": 2024,
      "type": "Conference Paper",
      "title": "Versatility of low-resolution tactile sensing for edge and pose detection",
      "authors": "Shepherd D., Husbands P., Johnson C., et al.",
      "venue": "IEEE AIRC 2024",
      "doi": "10.1109/AIRC61399.2024.10671677"
    },
    {
      "year": 2023,
      "type": "Conference Paper",
      "title": "Low-resolution sensing for sim-to-real complex terrain robots",
      "authors": "Shepherd D., Knight J.",
      "venue": "Towards Autonomous Robotic Systems (LNCS)",
      "doi": "10.1007/978-3-031-43360-3_16"
    },
    {
      "year": 2023,
      "type": "Preprint",
      "title": "Slip Detection and Surface Prediction Through Bio-Inspired Tactile Feedback",
      "authors": "Shepherd D., Husbands P., Johnson C., et al.",
      "venue": "arXiv (Cornell University)",
      "doi": "10.48550/arXiv.2310.08192"
    },
    {
      "year": 2023,
      "type": "Dissertation",
      "title": "Bio-Inspired Robotic Navigation On Varied Terrain",
      "authors": "Shepherd D.",
      "venue": "ResearchGate",
      "doi": "10.13140/RG.2.2.26032.16646"
    },
    {
      "year": 2022,
      "type": "Conference Paper",
      "title": "Evolving complex terrain navigation: emergent contour following from a low-resolution sensor",
      "authors": "Shepherd D., Knight J.",
      "venue": "UKRAS 2022",
      "doi": "10.31256/yp7gw5i"
    }
  ],
  "events": [
    {
      "year": 2026,
      "event": "ICRA",
      "city": "Vienna",
      "country": "Austria",
      "role": "Attendee"
    },
    {
      "year": 2025,
      "event": "RoboSoft",
      "city": "Lausanne",
      "country": "Switzerland",
      "role": "Poster presentation",
      "links": [
        {
          "label": "Extended abstract (PDF)",
          "url": "downloads/Robosoft_extended_abstract (3).pdf"
        }
      ]
    },
    {
      "year": 2024,
      "event": "Robotics: Science and Systems (RSS)",
      "city": "Delft",
      "country": "Netherlands",
      "role": "Poster presentation",
      "links": [
        {
          "label": "Abstract (PDF)",
          "url": "downloads/Robotics__Science_and_Systems_Conference2024 (4).pdf"
        }
      ]
    },
    {
      "year": 2024,
      "event": "IEEE Artificial Intelligence, Robotics and Control (AIRC)",
      "city": "Cairo",
      "country": "Egypt",
      "role": "Oral presentation",
      "award": "Best Presenter Award",
      "doi": "10.1109/AIRC61399.2024.10671677"
    },
    {
      "year": 2023,
      "event": "ICRA",
      "city": "London",
      "country": "United Kingdom",
      "role": "Attendee"
    },
    {
      "year": 2023,
      "event": "UKRAS Conference",
      "city": "Cambridge",
      "country": "United Kingdom",
      "role": "Poster presentation",
      "doi": "10.1007/978-3-031-43360-3_16"
    },
    {
      "year": 2023,
      "event": "Robotics Summer School (MILA)",
      "city": "Montreal",
      "country": "Canada",
      "role": "Participant"
    },
    {
      "year": 2022,
      "event": "Insect-Inspired Technologies Conference",
      "city": "Edinburgh",
      "country": "United Kingdom",
      "role": "Attendee"
    },
    {
      "year": 2026,
      "event": "ARIA Workshop on Robot Locomotion",
      "city": "York",
      "country": "United Kingdom",
      "role": "Attendee"
    },
    {
      "year": 2022,
      "event": "UKRAS",
      "city": "Aberystwyth",
      "country": "United Kingdom",
      "role": "Paper presentation",
      "award": "Best Paper Award",
      "links": [
        {
          "label": "Paper (PDF)",
          "url": "downloads/Bio_Inspired_Paper (1).pdf"
        }
      ]
    }
  ]
};


/* ================= PART 2: CODE ================= */


(function () {
  "use strict";

  /* ---------- small helpers ---------- */

  function el(tag, attrs, children) {
    const node = document.createElement(tag);
    Object.entries(attrs || {}).forEach(([k, v]) => {
      if (v === null || v === undefined) return;
      if (k === "text") node.textContent = v;
      else node.setAttribute(k, v);
    });
    (children || []).forEach(c => c && node.appendChild(c));
    return node;
  }

  // Turn the optional `doi` field and the `links` array into one list of links.
  function collectLinks(item) {
    const links = (item.links || []).slice();
    if (item.doi) {
      links.push({ label: "DOI", url: "https://doi.org/" + item.doi });
    }
    return links;
  }

  function linkRow(item, name) {
    const links = collectLinks(item);
    if (!links.length) return null;
    const p = el("p", { "class": "pub-links" });
    links.forEach(l => {
      p.appendChild(el("a", {
        href: encodeURI(l.url),
        // visible text comes first so the accessible name still contains it
        "aria-label": l.label + " for " + name
      }, [document.createTextNode(l.label)]));
    });
    return p;
  }

  // Newest year first; entries in the same year keep the order they have in the JSON.
  function groupByYear(items) {
    const groups = new Map();
    items
      .map((item, i) => ({ item, i }))
      .sort((a, b) => b.item.year - a.item.year || a.i - b.i)
      .forEach(({ item }) => {
        if (!groups.has(item.year)) groups.set(item.year, []);
        groups.get(item.year).push(item);
      });
    return groups;
  }

  function renderGrouped(container, items, idPrefix, renderItem) {
    container.replaceChildren();
    groupByYear(items).forEach((group, year) => {
      const headingId = idPrefix + "-" + year;
      const ul = el("ul", { "class": "pub-items", "aria-labelledby": headingId });
      group.forEach(item => ul.appendChild(renderItem(item)));
      container.appendChild(el("div", { "class": "year-group" }, [
        el("h3", { id: headingId, text: year }),
        ul
      ]));
    });
  }

  /* ---------- publications ---------- */

  // Your name as it appears in the author lists; it is shown in bold.
  const MY_NAME = "Shepherd D.";

  function authorsNode(text) {
    const p = el("p", { "class": "pub-authors" });
    const parts = text.split(MY_NAME);
    parts.forEach((part, i) => {
      if (part) p.appendChild(document.createTextNode(part));
      if (i < parts.length - 1) p.appendChild(el("strong", { text: MY_NAME }));
    });
    return p;
  }

  function renderPublication(p) {
    return el("li", { "class": "pub-item", "data-type": p.type }, [
      el("span", { "class": "pub-type", text: p.type }),
      el("span", { "class": "pub-title", text: p.title }),
      authorsNode(p.authors),
      el("p", { "class": "pub-venue", text: p.venue }),
      linkRow(p, p.title)
    ]);
  }

  function setupPublications(pubs) {
    const list = document.getElementById("pub-list");
    const filters = document.getElementById("pub-filters");
    const status = document.getElementById("pub-status");

    const types = ["All"].concat([...new Set(pubs.map(p => p.type))]);
    let active = "All";

    function draw() {
      const shown = active === "All" ? pubs : pubs.filter(p => p.type === active);
      renderGrouped(list, shown, "pub-year", renderPublication);
      status.textContent = "Showing " + shown.length + " of " + pubs.length +
        (active === "All" ? " items." : " items of type " + active + ".");
      filters.querySelectorAll("button").forEach(b =>
        b.setAttribute("aria-pressed", String(b.dataset.type === active)));
    }

    types.forEach(type => {
      const n = type === "All" ? pubs.length : pubs.filter(p => p.type === type).length;
      const b = el("button", { type: "button", "data-type": type }, [
        document.createTextNode(type),
        el("span", { "class": "count", text: n })
      ]);
      b.addEventListener("click", () => { active = type; draw(); });
      filters.appendChild(b);
    });
    draw();
  }

  /* ---------- events ---------- */

  function renderEvent(e) {
    const place = [e.city, e.country].filter(Boolean).join(", ");
    const award = e.award
      ? el("span", { "class": "pub-award" }, [
          el("span", { "class": "visually-hidden", text: "Award: " }),
          document.createTextNode(e.award)
        ])
      : null;
    return el("li", { "class": "pub-item" }, [
      el("span", { "class": "pub-title", text: e.event }),
      el("p", { "class": "pub-venue", text: e.role + " in " + place }),
      award,
      linkRow(e, e.event)
    ]);
  }

  /* ---------- start ---------- */

  const data = SITE_DATA;
  setupPublications(data.publications);
  renderGrouped(document.getElementById("event-list"), data.events, "event-year", renderEvent);
})();

