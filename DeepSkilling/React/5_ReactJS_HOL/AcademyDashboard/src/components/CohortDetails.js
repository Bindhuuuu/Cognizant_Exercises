// CohortDetails.js
// ---------------------------------------------------------------
// Component: CohortDetails
// Purpose  : Displays details of a single cohort inside a styled card.
// Styling  :
//   - CSS Module  → className={styles.box} for the card container
//   - Inline style → color applied to cohort name based on status
//     • "ongoing"   → green
//     • "completed" → blue
// ---------------------------------------------------------------

import React from 'react';

// Import the CSS Module — styles are locally scoped to this component
import styles from '../CohortDetails.module.css';

// CohortDetails receives a single cohort object as a prop
function CohortDetails({ cohort }) {
  // Destructure the cohort object for easy access
  const { name, technology, startDate, status } = cohort;

  // ── Inline style: colour the cohort name based on its status ──
  // If status is "ongoing" → green, otherwise → blue
  const nameStyle = {
    color: status.toLowerCase() === 'ongoing' ? 'green' : 'blue',
  };

  return (
    // Apply CSS Module class "box" to the card container div
    <div className={styles.box}>

      {/* Cohort name heading with inline colour based on status */}
      <h3 style={nameStyle}>{name}</h3>

      {/*
        Display cohort details using a definition list:
          <dl>  → definition list container
          <dt>  → term / label  (bold via CSS Module)
          <dd>  → description / value
      */}
      <dl>
        <dt>Technology</dt>
        <dd>{technology}</dd>

        <dt>Start Date</dt>
        <dd>{startDate}</dd>

        <dt>Status</dt>
        <dd style={nameStyle}>{status}</dd>
      </dl>
    </div>
  );
}

export default CohortDetails;
