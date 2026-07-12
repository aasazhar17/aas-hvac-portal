/**
 * AAS Air Conditioning and Engineering - Client Logic & API Connections (2026)
 */

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initHeaderAndScroll();
    initCounters();
    initScrollReveal();
    initProductCatalog();
    initTestimonialSlider();
    initFaqAccordion();
    initModals();
    initChatbot();
    initCalculator();
});

/* ==========================================================================
   1. Dataset: HVAC Products (Extracted from PDF Catalog)
   ========================================================================== */
const PRODUCTS_DATA = [
    {
        id: 'screw-chiller',
        name: 'AAS Screw Chiller',
        category: 'chillers',
        image: 'assets/images/chiller.png',
        badge: 'High Capacity',
        desc: 'Designed for uninterruptible industrial operations in extreme tropical climates with capacity control and high-efficiency European screw compressors.',
        specs: {
            'Compressor Type': 'Reliable European Screw Compressor (ARI tested)',
            'System Type': 'Available in DX (Direct Expansion) & Flooded systems',
            'Features': 'Capacity control, tropicalized condensing unit, eco-friendly refrigerants',
            'Typical Applications': 'Chemical, pharmaceutical, rubber, and heavy process industries'
        }
    },
    {
        id: 'scroll-chiller',
        name: 'AAS Scroll Chiller',
        category: 'chillers',
        image: 'assets/images/chiller.png',
        badge: 'ISO Certified',
        desc: 'Modular scroll chillers configured with integrated water tank and circulation pumps for fast plug-and-play installation.',
        specs: {
            'Controls': 'Microprocessor-based digital system',
            'Design Standard': 'ISO 9001:2015 certified manufacturing unit',
            'Configuration': 'Built-in storage tank & water circulation pump',
            'Advantages': 'Compact footprint, low noise emissions, easy maintenance'
        }
    },
    {
        id: 'inverter-chiller',
        name: 'AAS Inverter Chiller',
        category: 'chillers',
        image: 'assets/images/chiller.png',
        badge: 'Up to 40% Savings',
        desc: 'Advanced chilling units regulating compressor RPM dynamically to match variable process loads, saving significant energy costs.',
        specs: {
            'Technology': 'Dynamic frequency drive inverter controls',
            'Energy Saving': 'Up to 40% annual electricity bill reduction',
            'Startup Current': 'Smooth soft-start curve with no heavy current spikes',
            'Protection': 'Under/over voltage and phase loss protection built-in'
        }
    },
    {
        id: 'recip-chiller',
        name: 'AAS Recip Chiller',
        category: 'chillers',
        image: 'assets/images/chiller.png',
        badge: 'Low Maintenance',
        desc: 'Heavy-duty reciprocating compressor chillers designed to withstand high ambient temperatures with low initial capital investment.',
        specs: {
            'Compressor Style': 'Industrial Reciprocating Compressor',
            'Maintenance': 'Extremely low maintenance cost with simple serviceable parts',
            'Ambient Range': 'Engineered to withstand extreme ambient temperatures',
            'Durability': 'Robust structural steel base frame'
        }
    },
    {
        id: 'bulk-milk-cooler',
        name: 'Bulk Milk Cooler (BMC)',
        category: 'dairy',
        image: 'assets/images/cold_store.png',
        badge: 'Dairy Special',
        desc: 'Direct expansion (DX) milk cooling tanks (open & closed styles) designed for quick thermal drop to preserve milk quality.',
        specs: {
            'Capacities': 'Wide range from 500 liters to 5,000 liters',
            'Tank Material': 'Food-grade AISI-304 Stainless Steel with high-density insulation',
            'Agitator': 'Heavy-duty slow speed agitator with automatic cycle settings',
            'Options': 'Automatic CIP cleaning system, waste heat recovery coils'
        }
    },
    {
        id: 'cold-store',
        name: 'Prefabricated Cold Rooms',
        category: 'dairy',
        image: 'assets/images/cold_store.png',
        badge: 'High Density PUF',
        desc: 'Modular puff panel chambers assembled on-site with magnetic gaskets and digital control displays for temperature sensitive warehousing.',
        specs: {
            'Standard Temperature': '2°C to 4°C (Standard)',
            'Extreme Temperature': 'Deep freezing down to -18°C',
            'Panels': 'High-density PUF core wrapped in pre-painted G.I. sheet metal',
            'Safety': 'Door frame heaters for low temperature, emergency inner release handles'
        }
    },
    {
        id: 'air-washer',
        name: 'Air Washer & Pressurization',
        category: 'hvac',
        image: 'assets/images/hero.png',
        badge: 'Evaporative Cooling',
        desc: 'High-efficiency industrial evaporative air cooling units with cross-corrugated cellulose paper media and anti-vibration blowers.',
        specs: {
            'Cooling Pad': 'Cross-corrugated cellulose paper pads with anti-algae treat',
            'Structure': 'Double skin panels in G.I. or pre-coated sheets',
            'Blower Assembly': 'Dynamically balanced blowers mounted on anti-vibration bases',
            'Recommended For': 'Hotels, large production floors, plastic extrusion units, canteens'
        }
    },
    {
        id: 'air-handling-unit',
        name: 'Air Handling Unit (AHU)',
        category: 'hvac',
        image: 'assets/images/hero.png',
        badge: 'Modular Design',
        desc: 'Double-skinned modular AHUs intended for general ventilation, air filtration, and centralized cooling layouts in commercial structures.',
        specs: {
            'Mounting Options': 'Floor mounted, ceiling suspended, or loft installation',
            'Filters': 'Pre-filters (G.I. wiremesh) and fine synthetic media filters',
            'Bearings': 'Imported self-aligning pillow block bearings',
            'Casing': 'Aluminum profile frames with injected PUF panels'
        }
    },
    {
        id: 'ductable-ac',
        name: 'Ductable AC & Package Units',
        category: 'hvac',
        image: 'assets/images/hero.png',
        badge: '5TR to 20TR',
        desc: 'High-static package and ductable central air conditioners for commercial retail spaces, offices, and industrial workspace cooling.',
        specs: {
            'Capacity Range': '5 TR to 20 TR models available',
            'Mounting': 'Floor-standing and ceiling-suspended options',
            'Controls': 'Digital programmable microprocessor based',
            'Noise Levels': 'Optimized scroll compressor with acoustic lining for low noise'
        }
    },
    {
        id: 'ducting-insulation',
        name: 'Ducting & Thermal Insulation',
        category: 'hvac',
        image: 'assets/images/hero.png',
        badge: 'SMACNA Standards',
        desc: 'Precision-fabricated galvanized iron (G.I.) and aluminum air distribution ducting with premium insulation wrap overlays.',
        specs: {
            'Material': 'Galvanized steel sheets as per SMACNA parameters',
            'Insulation': 'Nitrile rubber or glass-wool insulation overlays',
            'Aesthetics': 'Perfect shape finishes with structural support hangers',
            'Grilles & Diffusers': 'Anodized aluminum supply and return air grilles'
        }
    },
    {
        id: 'electricals-electronics',
        name: 'Industrial Electrical Services',
        category: 'custom',
        image: 'assets/images/hero.png',
        badge: 'Turnkey Setup',
        desc: 'End-to-end design, cable routing, panel manufacturing, and site commissioning services for industrial electrical grids.',
        specs: {
            'Sectors Served': 'Commercial, industrial, dairy, and agricultural projects',
            'Scope': 'Design, electrical load calculations, MCC panel fabrication, commissioning',
            'Standard compliance': 'Compliance with standard Indian Electricity (IE) rules',
            'Team': 'Certified electrical engineers and project managers'
        }
    }
];

/* ==========================================================================
   2. Theme Switcher (Light / Dark Mode)
   ========================================================================== */
function initTheme() {
    const themeSwitchBtn = document.getElementById('theme-switch');
    if (!themeSwitchBtn) return;
    
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
    }
    
    themeSwitchBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        let newTheme = 'light';
        if (currentTheme === 'light') {
            newTheme = 'dark';
        }
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
}

/* ==========================================================================
   3. Header, Mobile Menu & Scroll progress
   ========================================================================== */
function initHeaderAndScroll() {
    const header = document.getElementById('main-header');
    const scrollBar = document.getElementById('scroll-bar');
    const backToTopBtn = document.getElementById('back-to-top-btn');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const navMenu = document.getElementById('nav-menu');
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        
        if (scrollTop > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        if (docHeight > 0) {
            const scrollPercentage = (scrollTop / docHeight) * 100;
            scrollBar.style.width = scrollPercentage + '%';
        }
        
        if (scrollTop > 500) {
            backToTopBtn.classList.add('active');
        } else {
            backToTopBtn.classList.remove('active');
        }
    });

    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenuBtn.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenuBtn.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }
}

/* ==========================================================================
   4. Stat Counter Animations (Count Up)
   ========================================================================== */
function initCounters() {
    const statNumbers = document.querySelectorAll('.stat-number');
    if (statNumbers.length === 0) return;

    const runCounters = () => {
        statNumbers.forEach(stat => {
            const target = parseInt(stat.getAttribute('data-target'));
            let count = 0;
            const duration = 2000;
            const stepTime = Math.max(Math.floor(duration / target), 10);
            
            const timer = setInterval(() => {
                count += Math.ceil(target / (duration / stepTime));
                if (count >= target) {
                    stat.textContent = target + (target === 100 ? '%' : '+');
                    clearInterval(timer);
                } else {
                    stat.textContent = count;
                }
            }, stepTime);
        });
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                runCounters();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    const statsSection = document.querySelector('.stats-banner');
    if (statsSection) {
        observer.observe(statsSection);
    }
}

/* ==========================================================================
   5. Scroll Reveal Animation Trigger
   ========================================================================== */
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.reveal-on-scroll');
    if (revealElements.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, { threshold: 0.15 });

    revealElements.forEach(el => observer.observe(el));
}

/* ==========================================================================
   6. Product Catalog Display & Category Filters
   ========================================================================== */
function initProductCatalog() {
    const catalogGrid = document.getElementById('product-catalog-grid');
    if (!catalogGrid) return;

    const displayProducts = (filterCategory) => {
        catalogGrid.innerHTML = '';
        
        const filtered = PRODUCTS_DATA.filter(prod => {
            return filterCategory === 'all' || prod.category === filterCategory;
        });

        filtered.forEach(prod => {
            const card = document.createElement('div');
            card.className = 'product-item-card reveal-on-scroll revealed';
            card.innerHTML = `
                <div class="product-item-image" style="background-image: url('${prod.image}');"></div>
                <div class="product-item-content">
                    <h3 style="font-size: 1.2rem; margin-bottom: 0.5rem; color: var(--text-headings);">${prod.name}</h3>
                    <p class="product-item-desc">${prod.desc}</p>
                    <div class="product-item-actions">
                        <button class="btn-download-pdf open-catalog-btn" style="border:none; background:none; cursor:pointer;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                            Catalog
                        </button>
                        <button class="btn-card-action view-spec-btn" data-id="${prod.id}">
                            View Specs
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                        </button>
                    </div>
                </div>
            `;
            catalogGrid.appendChild(card);
        });

        attachSpecListeners();
    };

    const filterBtns = document.querySelectorAll('.category-item');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const filterVal = btn.getAttribute('data-filter');
            displayProducts(filterVal);
        });
    });

    displayProducts('all');
}

/* ==========================================================================
   7. Product Specification Modal Viewer
   ========================================================================== */
function attachSpecListeners() {
    const specBtns = document.querySelectorAll('.view-spec-btn');
    const specModal = document.getElementById('spec-modal');
    const specTitle = document.getElementById('spec-title');
    const specBody = document.getElementById('spec-body');
    const specModalClose = document.getElementById('spec-modal-close');

    if (!specModal || !specTitle || !specBody) return;

    specBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const prodId = btn.getAttribute('data-id');
            const product = PRODUCTS_DATA.find(p => p.id === prodId);
            
            if (product) {
                specTitle.textContent = product.name;
                
                let specsHTML = `<p style="margin-bottom:1.5rem; font-size:1rem;">${product.desc}</p>`;
                specsHTML += `<div style="display:flex; flex-direction:column; gap:1rem;">`;
                
                for (const [key, value] of Object.entries(product.specs)) {
                    specsHTML += `
                        <div style="border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
                            <strong style="color: var(--text-headings); font-size: 0.9rem; display:block; margin-bottom:0.25rem;">${key}</strong>
                            <span style="font-size:0.9rem; color:var(--text-muted);">${value}</span>
                        </div>
                    `;
                }
                specsHTML += `</div>`;
                specsHTML += `
                    <div style="margin-top:2.5rem; text-align:right;">
                        <button class="btn btn-primary btn-card modal-inquire-trigger" data-name="${product.name}">Inquire for this System</button>
                    </div>
                `;
                
                specBody.innerHTML = specsHTML;
                specModal.classList.add('active');

                const subInquireBtn = specBody.querySelector('.modal-inquire-trigger');
                if (subInquireBtn) {
                    subInquireBtn.addEventListener('click', () => {
                        specModal.classList.remove('active');
                        openQuoteModal(product.name);
                    });
                }
            }
        });
    });

    if (specModalClose) {
        specModalClose.addEventListener('click', () => {
            specModal.classList.remove('active');
        });
    }
}

/* ==========================================================================
   8. Testimonial Carousel Slider
   ========================================================================== */
function initTestimonialSlider() {
    const track = document.getElementById('testimonial-track-container');
    const prevBtn = document.getElementById('prev-test-btn');
    const nextBtn = document.getElementById('next-test-btn');
    if (!track || !prevBtn || !nextBtn) return;

    const slides = Array.from(track.children);
    let currentIndex = 0;

    const updateSlider = (index) => {
        track.style.transform = `translateX(-${index * 100}%)`;
    };

    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % slides.length;
        updateSlider(currentIndex);
    });

    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        updateSlider(currentIndex);
    });
}

/* ==========================================================================
   9. FAQ Accordion Panels
   ========================================================================== */
function initFaqAccordion() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            faqItems.forEach(i => i.classList.remove('active'));
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
}

/* ==========================================================================
   10. Interactive Chilling Load Calculator
   ========================================================================== */
function initCalculator() {
    const calcForm = document.getElementById('chiller-calculator-form');
    const placeholder = document.getElementById('calc-placeholder');
    const resultDisplay = document.getElementById('calc-display');
    const calculatedTr = document.getElementById('calculated-tr');
    const calculatedKw = document.getElementById('calculated-kw');
    const recommendedProduct = document.getElementById('recommended-product-name');
    const recommendedDesc = document.getElementById('recommended-product-desc');
    const briefFlow = document.getElementById('spec-brief-flow');
    const briefDelta = document.getElementById('spec-brief-delta');

    if (!calcForm) return;

    calcForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const industry = document.getElementById('industry-select').value;
        const flowVal = parseFloat(document.getElementById('flow-rate').value);
        const flowUnit = document.getElementById('flow-unit').value;
        const inletT = parseFloat(document.getElementById('inlet-temp').value);
        const outletT = parseFloat(document.getElementById('outlet-temp').value);

        if (outletT >= inletT) {
            alert('Outlet Temperature must be lower than Inlet Temperature for chilling calculation.');
            return;
        }

        // Convert GPM to LPM if selected
        let flowLPM = flowVal;
        if (flowUnit === 'gpm') {
            flowLPM = flowVal * 3.78541;
        }

        const deltaT = inletT - outletT;
        
        // Heat load formula: Q (kcal/h) = LPM * 60 * 1 * deltaT
        // Tons of Refrigeration (TR) = Q / 3024
        const kcalHr = flowLPM * 60 * 1 * deltaT;
        const tr = kcalHr / 3024;
        const kw = tr * 3.517; // 1 TR = 3.517 kW

        // Determine recommended product
        let prodName = "AAS Scroll Chiller";
        let prodDesc = "Ideal standard process chiller with integrated steel tank and circulation pump.";

        if (tr > 60) {
            prodName = "AAS Screw Chiller";
            prodDesc = "Heavy-duty system featuring European compressors and capacity configuration options.";
        } else if (industry === 'dairy') {
            prodName = "AAS Bulk Milk Cooler (BMC)";
            prodDesc = "Direct expansion (DX) milk cooling tank configured with agitating controllers.";
        } else if (tr < 15 && (industry === 'plastic' || industry === 'pharma')) {
            prodName = "AAS Inverter Chiller";
            prodDesc = "Variable speed dynamic scroll chiller yielding up to 40% annual electricity bill savings.";
        }

        // Update DOM
        calculatedTr.innerHTML = `${tr.toFixed(2)} <span>TR</span>`;
        calculatedKw.textContent = `Equivalent to ${kw.toFixed(2)} kW of cooling capacity`;
        recommendedProduct.textContent = prodName;
        recommendedDesc.textContent = prodDesc;
        briefFlow.textContent = `${flowVal} ${flowUnit.toUpperCase()}`;
        briefDelta.textContent = `${deltaT.toFixed(1)} °C`;

        placeholder.style.display = 'none';
        resultDisplay.style.display = 'block';

        // Bind Quote Button action within calculator
        const calcQuoteBtn = document.getElementById('quote-btn-calc');
        if (calcQuoteBtn) {
            calcQuoteBtn.onclick = (event) => {
                event.preventDefault();
                openQuoteModal(prodName);
            };
        }
    });
}

/* ==========================================================================
   11. API Connection Modals (Quote, Catalog, Specs)
   ========================================================================== */
let openQuoteModal = () => {}; 

function initModals() {
    const inquiryModal = document.getElementById('inquiry-modal');
    const inquiryModalClose = document.getElementById('inquiry-modal-close');
    const catalogModal = document.getElementById('catalog-modal');
    const catalogModalClose = document.getElementById('catalog-modal-close');
    
    const quoteBtns = [
        document.getElementById('header-quote-btn'),
        document.getElementById('hero-quote-btn')
    ];

    openQuoteModal = (productPresetName = '') => {
        if (!inquiryModal) return;
        const selectBox = document.getElementById('usr-product');
        if (selectBox && productPresetName) {
            const lowerName = productPresetName.toLowerCase();
            if (lowerName.includes('screw')) selectBox.value = 'screw_chiller';
            else if (lowerName.includes('scroll')) selectBox.value = 'scroll_chiller';
            else if (lowerName.includes('inverter')) selectBox.value = 'inverter_chiller';
            else if (lowerName.includes('milk') || lowerName.includes('cooler')) selectBox.value = 'milk_cooler';
            else if (lowerName.includes('cold') || lowerName.includes('store') || lowerName.includes('room')) selectBox.value = 'cold_room';
            else if (lowerName.includes('washer')) selectBox.value = 'air_washer';
            else if (lowerName.includes('ahu') || lowerName.includes('handling')) selectBox.value = 'ahu';
            else if (lowerName.includes('ducting')) selectBox.value = 'ducting';
        }
        inquiryModal.classList.add('active');
    };

    quoteBtns.forEach(btn => {
        if (btn) {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                openQuoteModal();
            });
        }
    });

    if (inquiryModalClose) {
        inquiryModalClose.addEventListener('click', () => {
            inquiryModal.classList.remove('active');
        });
    }

    document.addEventListener('click', (e) => {
        if (e.target && e.target.closest('.open-catalog-btn')) {
            e.preventDefault();
            if (catalogModal) catalogModal.classList.add('active');
        }
    });

    if (catalogModalClose) {
        catalogModalClose.addEventListener('click', () => {
            catalogModal.classList.remove('active');
        });
    }

    // --- Backend API Form Submissions ---

    // 1. Home Contact Form
    const b2bForm = document.getElementById('b2b-inquiry-form');
    const successMsg = document.getElementById('inquiry-success-msg');
    if (b2bForm && successMsg) {
        b2bForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                name: document.getElementById('usr-name').value,
                company: document.getElementById('usr-company').value,
                email: document.getElementById('usr-email').value,
                phone: document.getElementById('usr-phone').value,
                city: document.getElementById('usr-city').value,
                product: document.getElementById('usr-product').value,
                message: document.getElementById('usr-message').value
            };

            try {
                const response = await fetch('/api/inquiry', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    successMsg.style.display = 'block';
                    b2bForm.reset();
                    setTimeout(() => { successMsg.style.display = 'none'; }, 6000);
                } else {
                    const err = await response.json();
                    alert('Inquiry failed: ' + (err.detail || 'Server error'));
                }
            } catch (err) {
                alert('Connection error. Could not reach database api.');
            }
        });
    }

    // 2. Modal Quote Form
    const modalForm = document.getElementById('modal-quote-form');
    const modalSuccess = document.getElementById('modal-success-msg');
    if (modalForm && modalSuccess) {
        modalForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                name: document.getElementById('m-name').value,
                company: document.getElementById('m-company').value,
                email: document.getElementById('m-email').value,
                phone: document.getElementById('m-phone').value,
                city: 'Modal Inquiry',
                product: document.getElementById('usr-product') ? document.getElementById('usr-product').value : 'other',
                message: document.getElementById('m-message').value
            };

            try {
                const response = await fetch('/api/inquiry', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    modalSuccess.style.display = 'block';
                    modalForm.reset();
                    setTimeout(() => {
                        modalSuccess.style.display = 'none';
                        inquiryModal.classList.remove('active');
                    }, 3000);
                } else {
                    const err = await response.json();
                    alert('Inquiry failed: ' + (err.detail || 'Server error'));
                }
            } catch (err) {
                alert('Connection error.');
            }
        });
    }

    // 3. Catalog Download Form
    const catalogForm = document.getElementById('modal-catalog-form');
    const catalogSuccess = document.getElementById('catalog-success-msg');
    if (catalogForm && catalogSuccess) {
        catalogForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('c-email').value;

            try {
                const response = await fetch('/api/catalog-download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email })
                });

                if (response.ok) {
                    catalogSuccess.style.display = 'block';
                    catalogForm.reset();
                    
                    // Simulate catalog PDF generation
                    setTimeout(() => {
                        catalogSuccess.style.display = 'none';
                        catalogModal.classList.remove('active');
                        // Download the official company PDF catalog
                        const link = document.createElement('a');
                        link.href = '/AAS_Catalog_2026.pdf';
                        link.download = 'AAS_Air_Conditioning_Catalog_2026.pdf';
                        link.click();
                    }, 2000);
                } else {
                    alert('Submission failed.');
                }
            } catch (err) {
                alert('Connection error.');
            }
        });
    }
}

/* ==========================================================================
   12. Smart Sales Assistant Chatbot API Integration
   ========================================================================== */
function initChatbot() {
    const chatbotToggleBtn = document.getElementById('chatbot-toggle-btn');
    const chatbotPanel = document.getElementById('chatbot-panel-box');
    const chatbotCloseBtn = document.getElementById('chatbot-close-btn');
    const messagesContainer = document.getElementById('chatbot-messages');
    const textInput = document.getElementById('chatbot-text-input');
    const sendBtn = document.getElementById('chatbot-send-btn');
    const suggestionsBox = document.getElementById('chatbot-suggestions');

    if (!chatbotToggleBtn || !chatbotPanel || !chatbotCloseBtn || !messagesContainer) return;

    chatbotToggleBtn.addEventListener('click', () => {
        chatbotPanel.classList.toggle('active');
    });

    chatbotCloseBtn.addEventListener('click', () => {
        chatbotPanel.classList.remove('active');
    });

    const printBotMessage = (text) => {
        const msg = document.createElement('div');
        msg.className = 'chat-message message-bot';
        msg.innerHTML = text;
        messagesContainer.appendChild(msg);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Attach click action to quote buttons inside bot answers
        const quoteBtn = msg.querySelector('.chatbot-inquire');
        if (quoteBtn) {
            quoteBtn.addEventListener('click', () => {
                chatbotPanel.classList.remove('active');
                openQuoteModal();
            });
        }
    };

    const printUserMessage = (text) => {
        const msg = document.createElement('div');
        msg.className = 'chat-message message-user';
        msg.textContent = text;
        messagesContainer.appendChild(msg);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };

    // Post to FastAPI backend `/api/chat`
    const sendQueryToBackend = async (queryText) => {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: queryText })
            });
            
            if (response.ok) {
                const data = await response.json();
                printBotMessage(data.response);
            } else {
                printBotMessage("I am experiencing network connectivity issues. Please try calling +91-9999404742.");
            }
        } catch (err) {
            printBotMessage("Server API connection offline. Please check that uvicorn is running.");
        }
    };

    // Suggested queries click handlers
    if (suggestionsBox) {
        suggestionsBox.addEventListener('click', (e) => {
            if (e.target && e.target.classList.contains('suggested-btn')) {
                const queryText = e.target.textContent;
                printUserMessage(queryText);
                setTimeout(() => {
                    sendQueryToBackend(queryText);
                }, 400);
            }
        });
    }

    const handleTextQuery = () => {
        const text = textInput.value.trim();
        if (!text) return;

        printUserMessage(text);
        textInput.value = '';

        setTimeout(() => {
            sendQueryToBackend(text);
        }, 300);
    };

    sendBtn.addEventListener('click', handleTextQuery);
    textInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleTextQuery();
        }
    });
}
