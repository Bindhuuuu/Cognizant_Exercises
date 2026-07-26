// App.js
// ---------------------------------------------------------------
// Root Component: App
// Purpose : Holds the cohort data and renders all CohortDetails cards.
//
// Data    : 4 sample cohorts (2 Ongoing, 2 Completed)
// Layout  : Inline styles used on the page-level container and header
// ---------------------------------------------------------------

import React from 'react';
import CohortDetails from './components/CohortDetails';

// ── Sample cohort data ──────────────────────────────────────────
// Contains 2 ongoing and 2 completed cohorts for the dashboard.
const cohorts = [
  {
    id: 1,
    name: 'Java Full Stack Batch 12',
    technology: 'Java, Spring Boot, React',
    startDate: '01 March 2025',
    status: 'Ongoing',
  },
  {
    id: 2,
    name: 'Cloud & DevOps Batch 7',
    technology: 'AWS, Docker, Kubernetes',
    startDate: '15 April 2025',
    status: 'Ongoing',
  },
  {
    id: 3,
    name: 'Python Data Science Batch 5',
    technology: 'Python, Pandas, Machine Learning',
    startDate: '10 January 2025',
    status: 'Completed',
  },
  {
    id: 4,
    name: '.NET Enterprise Batch 9',
    technology: 'C#, ASP.NET Core, Azure',
    startDate: '05 November 2024',
    status: 'Completed',
  },
];

// ── Inline styles for the App-level layout ──────────────────────
// These demonstrate inline styling at the page/container level.
const pageStyle = {
  fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
  minHeight: '100vh',
  backgroundColor: '#f0f2f5',
  padding: '30px 20px',
};

const headerStyle = {
  textAlign: 'center',
  marginBottom: '30px',
};

const titleStyle = {
  fontSize: '2rem',
  fontWeight: '700',
  color: '#1a1a2e',
  margin: '0 0 6px 0',
};

const subtitleStyle = {
  fontSize: '1rem',
  color: '#555555',
  margin: 0,
};

const dividerStyle = {
  width: '60px',
  height: '4px',
  backgroundColor: '#0078d4',
  margin: '12px auto 0 auto',
  borderRadius: '2px',
};

const cardsContainerStyle = {
  textAlign: 'center', // centers inline-block cards
};

// ── App Component ───────────────────────────────────────────────
function App() {
  return (
    <div style={pageStyle}>

      {/* Page Header */}
      <header style={headerStyle}>
        <h1 style={titleStyle}>Cognizant Academy Dashboard</h1>
        <p style={subtitleStyle}>Ongoing &amp; Completed Cohort Overview</p>
        <div style={dividerStyle}></div>
      </header>

      {/* Cohort Cards Container */}
      <main style={cardsContainerStyle}>
        {/*
          Map over the cohorts array.
          Each cohort is passed as a prop to <CohortDetails />.
          The "key" prop is required by React for list rendering.
        */}
        {cohorts.map((cohort) => (
          <CohortDetails key={cohort.id} cohort={cohort} />
        ))}
      </main>

    </div>
  );
}

export default App;
