import React, { useState, useEffect } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import accessibility from 'highcharts/modules/accessibility';

if (typeof accessibility === 'function') {
  accessibility(Highcharts);
}

export default function App() {
  const [overall, setOverall] = useState(null);
  const [topics, setTopics] = useState([]);
  const [difficulty, setDifficulty] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [overallRes, topicsRes, diffRes] = await Promise.all([
          fetch('/api/v1/analytics/overall').then(r => r.ok ? r.json() : null),
          fetch('/api/v1/analytics/topics').then(r => r.ok ? r.json() : []),
          fetch('/api/v1/analytics/difficulty').then(r => r.ok ? r.json() : null)
        ]);
        setOverall(overallRes);
        setTopics(topicsRes);
        setDifficulty(diffRes);
      } catch (err) {
        console.error('Failed to fetch analytics:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const difficultyChartOptions = {
    chart: { type: 'pie', backgroundColor: 'transparent' },
    title: { text: 'Ingested Question Bank Distribution', style: { color: '#38bdf8', fontSize: '16px' } },
    accessibility: { enabled: true },
    credits: { enabled: false },
    plotOptions: {
      pie: {
        dataLabels: { enabled: true, format: '<b>{point.name}</b>: {point.y} questions', style: { color: '#f8fafc' } }
      }
    },
    series: [{
      name: 'Total Questions',
      colorByPoint: true,
      data: [
        { name: 'Easy', y: difficulty?.easy?.total || 0, color: '#4ade80' },
        { name: 'Medium', y: difficulty?.medium?.total || 0, color: '#fbbf24' },
        { name: 'Hard', y: difficulty?.hard?.total || 0, color: '#f87171' }
      ]
    }]
  };

  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '32px 16px' }}>
      <header style={{ borderBottom: '1px solid #334155', paddingBottom: '16px', marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ color: '#38bdf8', margin: 0, fontSize: '24px' }}>LeetCode Personal Analytics</h1>
          <p style={{ color: '#94a3b8', margin: '4px 0 0 0', fontSize: '14px' }}>Real-time Performance & Ingested Problem Bank</p>
        </div>
        <div style={{ background: '#1e293b', border: '1px solid #334155', padding: '8px 16px', borderRadius: '20px', fontSize: '13px', color: '#34d399', fontWeight: 'bold' }}>
          ✓ Database Synced Live
        </div>
      </header>

      {loading ? (
        <p style={{ color: '#94a3b8' }}>Loading live analytics dashboard...</p>
      ) : (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px', marginBottom: '32px' }}>
            <div style={{ background: '#1e293b', padding: '20px', borderRadius: '12px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', color: '#94a3b8', fontSize: '14px' }}>Total Ingested Problems</h3>
              <p style={{ fontSize: '28px', fontWeight: 'bold', color: '#38bdf8', margin: 0 }}>{overall?.total_problems || 0}</p>
            </div>

            <div style={{ background: '#1e293b', padding: '20px', borderRadius: '12px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', color: '#94a3b8', fontSize: '14px' }}>User Solved Count</h3>
              <p style={{ fontSize: '28px', fontWeight: 'bold', color: '#f8fafc', margin: 0 }}>{overall?.solved_count || 0}</p>
            </div>

            <div style={{ background: '#1e293b', padding: '20px', borderRadius: '12px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', color: '#94a3b8', fontSize: '14px' }}>Overall AC Rate</h3>
              <p style={{ fontSize: '28px', fontWeight: 'bold', color: '#34d399', margin: 0 }}>{overall?.overall_ac_rate || 0}%</p>
            </div>

            <div style={{ background: '#1e293b', padding: '20px', borderRadius: '12px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', color: '#94a3b8', fontSize: '14px' }}>Question Bank (E / M / H)</h3>
              <p style={{ fontSize: '18px', fontWeight: 'bold', color: '#38bdf8', margin: 0 }}>
                <span style={{ color: '#4ade80' }}>{difficulty?.easy?.total || 0}</span> / {' '}
                <span style={{ color: '#fbbf24' }}>{difficulty?.medium?.total || 0}</span> / {' '}
                <span style={{ color: '#f87171' }}>{difficulty?.hard?.total || 0}</span>
              </p>
            </div>
          </div>

          <div style={{ background: '#1e293b', padding: '24px', borderRadius: '12px', border: '1px solid #334155' }}>
            <HighchartsReact highcharts={Highcharts} options={difficultyChartOptions} />
          </div>
        </>
      )}
    </div>
  );
}
