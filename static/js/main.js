/**
 * Nishi Makeup Artist & Beauty Parlour - Main JavaScript
 * Handles dynamic booking prefill, live calculator, portfolio filters, modal previews, and mobile nav.
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Mobile Navigation Toggle
  const mobileToggle = document.getElementById('mobileNavToggle');
  const drawer = document.getElementById('mobileNavDrawer');
  const backdrop = document.getElementById('mobileNavBackdrop');
  const closeDrawerBtn = document.getElementById('closeDrawerBtn');

  function openDrawer() {
    if (drawer && backdrop) {
      drawer.classList.add('open');
      backdrop.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeDrawer() {
    if (drawer && backdrop) {
      drawer.classList.remove('open');
      backdrop.classList.remove('open');
      document.body.style.overflow = '';
    }
  }

  if (mobileToggle) mobileToggle.addEventListener('click', openDrawer);
  if (closeDrawerBtn) closeDrawerBtn.addEventListener('click', closeDrawer);
  if (backdrop) backdrop.addEventListener('click', closeDrawer);

  // Close drawer when any link is clicked
  const drawerLinks = document.querySelectorAll('.drawer-links a');
  drawerLinks.forEach(link => {
    link.addEventListener('click', closeDrawer);
  });

  // 2. Prevent past dates in appointment date input
  const dateInput = document.getElementById('appointment_date');
  if (dateInput) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', today);
  }

  // 3. Portfolio Gallery Filter
  const filterBtns = document.querySelectorAll('.gallery-filter-btn');
  const galleryCards = document.querySelectorAll('.gallery-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      filterBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');

      const filterVal = this.getAttribute('data-filter');

      galleryCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filterVal === 'all' || category === filterVal) {
          card.style.display = 'block';
          card.style.animation = 'fadeIn 0.4s ease forwards';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // 4. Service Category Filter Tabs (if on page)
  const serviceTabs = document.querySelectorAll('.service-tab-btn');
  const serviceCards = document.querySelectorAll('.service-card');

  serviceTabs.forEach(tab => {
    tab.addEventListener('click', function () {
      serviceTabs.forEach(t => t.classList.remove('active'));
      this.classList.add('active');

      const targetCat = this.getAttribute('data-category');

      serviceCards.forEach(sc => {
        const cat = sc.getAttribute('data-category');
        if (targetCat === 'all' || cat === targetCat) {
          sc.style.display = 'flex';
        } else {
          sc.style.display = 'none';
        }
      });
    });
  });

  // 5. Booking Form Live Summary & Interactivity
  const artistSelect = document.getElementById('artist-select');
  const serviceSelect = document.getElementById('service-select');
  const packageSelect = document.getElementById('package-select');

  const summaryArtist = document.getElementById('summary-artist');
  const summaryPackage = document.getElementById('summary-package');
  const summaryService = document.getElementById('summary-service');
  const summaryTotal = document.getElementById('summary-total');
  const summaryFeaturesBox = document.getElementById('summary-features-box');
  const summaryFeaturesList = document.getElementById('summary-features-list');

  // Parse embedded package and service data if available in window
  const packagesData = window.PACKAGES_DATA || {};
  const servicesData = window.SERVICES_DATA || {};

  function updateBookingSummary() {
    let totalBDT = 0;

    // Artist
    if (artistSelect && summaryArtist) {
      const selectedArtistName = artistSelect.options[artistSelect.selectedIndex]?.text || '--';
      summaryArtist.textContent = artistSelect.value ? selectedArtistName : 'Any Senior Stylist';
    }

    // Package
    let pkgSelected = false;
    if (packageSelect && summaryPackage) {
      const pkgId = packageSelect.value;
      if (pkgId && packagesData[pkgId]) {
        pkgSelected = true;
        const pkg = packagesData[pkgId];
        summaryPackage.textContent = pkg.name;
        totalBDT += pkg.price;

        if (summaryFeaturesBox && summaryFeaturesList) {
          summaryFeaturesBox.style.display = 'block';
          summaryFeaturesList.innerHTML = pkg.features
            .map(f => `<li>✓ ${f}</li>`)
            .join('');
        }
      } else {
        const fallbackText = packageSelect.options[packageSelect.selectedIndex]?.text;
        summaryPackage.textContent = packageSelect.value ? fallbackText : 'None Selected';
        if (summaryFeaturesBox) summaryFeaturesBox.style.display = 'none';
      }
    }

    // Service
    if (serviceSelect && summaryService) {
      const srvId = serviceSelect.value;
      if (srvId && servicesData[srvId]) {
        const srv = servicesData[srvId];
        summaryService.textContent = srv.name;
        if (!pkgSelected) {
          totalBDT += srv.price;
        }
      } else {
        const fallbackSrvText = serviceSelect.options[serviceSelect.selectedIndex]?.text;
        summaryService.textContent = serviceSelect.value ? fallbackSrvText : 'Standard Appointment';
      }
    }

    // Update total amount display
    if (summaryTotal) {
      summaryTotal.textContent = totalBDT > 0 ? `৳${totalBDT.toLocaleString()}` : '৳0';
    }
  }

  if (artistSelect) artistSelect.addEventListener('change', updateBookingSummary);
  if (serviceSelect) serviceSelect.addEventListener('change', updateBookingSummary);
  if (packageSelect) packageSelect.addEventListener('change', updateBookingSummary);

  // Initial call
  updateBookingSummary();

  // 6. Connect "Book This Artist" Buttons
  document.querySelectorAll('.btn-book-artist').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const artistId = this.getAttribute('data-artist-id');
      if (artistSelect && artistId) {
        artistSelect.value = artistId;
        updateBookingSummary();
      }
    });
  });

  // 7. Connect "Book This Service" Buttons
  document.querySelectorAll('.btn-book-service').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const serviceId = this.getAttribute('data-service-id');
      if (serviceSelect && serviceId) {
        serviceSelect.value = serviceId;
        updateBookingSummary();
      }
    });
  });

  // 8. Connect "Book This Package" Buttons
  document.querySelectorAll('.btn-book-package').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const packageId = this.getAttribute('data-package-id');
      if (packageSelect && packageId) {
        packageSelect.value = packageId;
        updateBookingSummary();
      }
    });
  });

  // 9. Artist Profile Preview Modal
  const artistModal = document.getElementById('artistProfileModal');
  const modalClose = document.getElementById('closeArtistModal');

  document.querySelectorAll('.btn-view-artist').forEach(btn => {
    btn.addEventListener('click', function () {
      const name = this.getAttribute('data-name');
      const title = this.getAttribute('data-title');
      const bio = this.getAttribute('data-bio');
      const photo = this.getAttribute('data-photo');
      const exp = this.getAttribute('data-exp');
      const rating = this.getAttribute('data-rating');
      const brides = this.getAttribute('data-brides');
      const specs = this.getAttribute('data-specs');
      const artistId = this.getAttribute('data-artist-id');

      document.getElementById('modalArtistName').textContent = name;
      document.getElementById('modalArtistTitle').textContent = title;
      document.getElementById('modalArtistBio').textContent = bio;
      document.getElementById('modalArtistPhoto').src = photo;
      document.getElementById('modalArtistExp').textContent = `${exp}+ Years`;
      document.getElementById('modalArtistRating').textContent = `${rating} ★`;
      document.getElementById('modalArtistBrides').textContent = `${brides}+ Brides`;

      // Specialties
      const specsContainer = document.getElementById('modalArtistSpecs');
      if (specsContainer && specs) {
        const specList = specs.split(',');
        specsContainer.innerHTML = specList
          .map(s => `<span class="spec-pill">${s.trim()}</span>`)
          .join('');
      }

      // Quick book button in modal
      const modalBookBtn = document.getElementById('modalBookArtistBtn');
      if (modalBookBtn && artistId) {
        modalBookBtn.setAttribute('data-artist-id', artistId);
        modalBookBtn.href = `#booking-section`;
        modalBookBtn.onclick = function () {
          if (artistSelect) {
            artistSelect.value = artistId;
            updateBookingSummary();
          }
          if (artistModal) artistModal.classList.remove('active');
        };
      }

      if (artistModal) artistModal.classList.add('active');
    });
  });

  if (modalClose && artistModal) {
    modalClose.addEventListener('click', () => artistModal.classList.remove('active'));
    artistModal.addEventListener('click', (e) => {
      if (e.target === artistModal) artistModal.classList.remove('active');
    });
  }

  // 10. Image Lightbox for Gallery
  const lightboxModal = document.getElementById('galleryLightboxModal');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxTitle = document.getElementById('lightboxTitle');
  const lightboxClose = document.getElementById('closeLightbox');

  document.querySelectorAll('.gallery-card').forEach(card => {
    card.addEventListener('click', function () {
      const img = this.querySelector('img').src;
      const title = this.querySelector('.gallery-item-title')?.textContent || 'Bridal Glamour';
      if (lightboxModal && lightboxImg) {
        lightboxImg.src = img;
        if (lightboxTitle) lightboxTitle.textContent = title;
        lightboxModal.classList.add('active');
      }
    });
  });

  if (lightboxClose && lightboxModal) {
    lightboxClose.addEventListener('click', () => lightboxModal.classList.remove('active'));
    lightboxModal.addEventListener('click', (e) => {
      if (e.target === lightboxModal) lightboxModal.classList.remove('active');
    });
  }

  // 11. Auto dismiss alerts after 5 seconds
  setTimeout(() => {
    const alerts = document.querySelectorAll('.custom-alert');
    alerts.forEach(alert => {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.5s ease';
      setTimeout(() => alert.remove(), 500);
    });
  }, 5000);
});
