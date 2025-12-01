// unauthorized-banner.js
// Simplified client-side helper to show an "Unauthorized" banner
// if the user's email (from ENV.USER_EMAIL) matches a blocked domain.

function initUnauthorizedBanner({ blockedDomains = [], bannerText = 'Unauthorized', subText = 'You do not have access to this site.' } = {}) {
  const email = getUserEmail();
  if (!email) return false;

  const domain = extractDomain(email);
  if (!domain) return false;

  const normalizedBlocked = new Set(blockedDomains.map(d => d.trim().toLowerCase()));
  if (!normalizedBlocked.has(domain)) return false;

  showUnauthorizedBanner({ bannerText, subText, domain });
  return true;
}

function getUserEmail() {
  try {
    if (typeof ENV !== 'undefined' && ENV.USER_EMAIL) {
      return String(ENV.USER_EMAIL).trim();
    }
  } catch (err) {
    console.warn('Could not read ENV.USER_EMAIL', err);
  }
  return null;
}

function extractDomain(email) {
  const atIdx = email.lastIndexOf('@');
  return atIdx !== -1 ? email.slice(atIdx + 1).toLowerCase() : null;
}

function showUnauthorizedBanner({ bannerText, subText, domain }) {
  document.head.innerHTML = '';
  document.body.innerHTML = '';

  const root = document.createElement('div');
  Object.assign(root.style, {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100vw',
    height: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 999999,
    background: 'linear-gradient(180deg, rgba(0,0,0,0.6), rgba(0,0,0,0.8))',
    color: '#fff',
    fontFamily: 'system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial',
    padding: '2rem',
    textAlign: 'center'
  });

  const card = document.createElement('div');
  Object.assign(card.style, {
    background: 'rgba(0,0,0,0.6)',
    backdropFilter: 'blur(6px)',
    borderRadius: '12px',
    boxShadow: '0 8px 30px rgba(0,0,0,0.7)',
    padding: '2rem',
    maxWidth: '720px',
    width: 'min(95%, 720px)'
  });

  const h1 = document.createElement('h1');
  h1.textContent = bannerText;
  h1.style.marginBottom = '0.5rem';
  h1.style.fontSize = 'clamp(1.5rem, 3vw, 2.25rem)';

  const p = document.createElement('p');
  p.textContent = `${subText} (domain: ${domain})`;
  p.style.marginTop = '0.25rem';

  const small = document.createElement('div');
  small.textContent = 'If you think this is a mistake, contact your administrator.';
  small.style.marginTop = '1rem';
  small.style.opacity = '0.8';
  small.style.fontSize = '0.9rem';

  card.append(h1, p, small);
  root.appendChild(card);
  document.body.appendChild(root);

  return true;
}

function runBanner() {
  try {
    initUnauthorizedBanner({
      blockedDomains: [''], // customise as needed
      bannerText: 'Unauthorized',
      subText: 'Access denied for your organisation.'
    });
  } catch (err) {
    console.error('Unauthorized banner script error', err);
  }
};

if (window.location.host.includes("beta")) {
  runBanner();
} else if (window.location.host.includes("test")) {
  runBanner();
} else {
  console.log("You're in production")
  }
