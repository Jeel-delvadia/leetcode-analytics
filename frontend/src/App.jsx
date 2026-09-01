import React, { useState, useEffect } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import accessibility from 'highcharts/modules/accessibility';

if (typeof accessibility === 'function') {
  accessibility(Highcharts);
}

export default function App() {
  const [overall, setOverall] = useState(null);
  const [difficulty, setDifficulty] = useState(null);
  const [tablesSummary, setTablesSummary] = useState([]);
  const [selectedTable, setSelectedTable] = useState('Problem');
  const [tableData, setTableData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [tableLoading, setTableLoading] = useState(false);
  const [page, setPage] = useState(1);
  const pageSize = 100;

  useEffect(() => {
    async function fetchData() {
      try {
        const [overallRes, diffRes, tablesRes] = await Promise.all([
          fetch('/api/v1/analytics/overall').then(r => r.ok ? r.json() : null),
          fetch('/api/v1/analytics/difficulty').then(r => r.ok ? r.json() : null),
          fetch('/api/v1/analytics/db/tables').then(r => r.ok ? r.json() : [])
        ]);
        setOverall(overallRes);
        setDifficulty(diffRes);
        setTablesSummary(tablesRes);
      } catch (err) {
        console.error('Failed to fetch analytics:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  useEffect(() => {
    if (!selectedTable) return;
    async function fetchTableRecords() {
      setTableLoading(true);
      try {
        // Fetch full table payload from backend
        const res = await fetch(`/api/v1/analytics/db/tables/${selectedTable}`);
        if (res.ok) {
          const data = await res.json();
          setTableData(data);
        } else {
          setTableData([]);
        }
      } catch (e) {
        console.error(`Error loading ${selectedTable}:`, e);
        setTableData([]);
      } finally {
        setTableLoading(false);
        setPage(1);
      }
    }
    fetchTableRecords();
  }, [selectedTable]);

  const difficultyChartOptions = {
    chart: { type: 'pie', backgroundColor: 'transparent' },
    title: { text: 'Ingested Problem Bank Distribution', style: { color: '#38bdf8', fontSize: '16px' } },
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

  const getTableColumns = () => {
    if (!tableData || tableData.length === 0) return [];
    return Object.keys(tableData[0]);
  };

  const totalRecords = tableData.length;
  const totalPages = Math.ceil(totalRecords / pageSize) || 1;
  const paginatedData = tableData.slice((page - 1) * pageSize, page * pageSize);

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '32px 16px', color: '#f8fafc', fontFamily: 'sans-serif' }}>
      <header style={{ borderBottom: '1px solid #334155', paddingBottom: '16px', marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ color: '#38bdf8', margin: 0, fontSize: '24px' }}>LeetCode Database & Analytics Inspector</h1>
          <p style={{ color: '#94a3b8', margin: '4px 0 0 0', fontSize: '14px' }}>Inspect Database Design Tables & Real-time Progress</p>
        </div>
        <div style={{ background: '#1e293b', border: '1px solid #334155', padding: '8px 16px', borderRadius: '20px', fontSize: '13px', color: '#34d399', fontWeight: 'bold' }}>
          ✓ Database Synced Live
        </div>
      </header>

      {loading ? (
        <p style={{ color: '#94a3b8' }}>Loading database analytics...</p>
      ) : (
        <>
          {/* Top Metric Cards */}
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
              <h3 style={{ margin: '0 0 8px 0', color: '#94a3b8', fontSize: '14px' }}>Difficulty (E / M / H)</h3>
              <p style={{ fontSize: '18px', fontWeight: 'bold', color: '#38bdf8', margin: 0 }}>
                <span style={{ color: '#4ade80' }}>{difficulty?.easy?.total || 0}</span> / {' '}
                <span style={{ color: '#fbbf24' }}>{difficulty?.medium?.total || 0}</span> / {' '}
                <span style={{ color: '#f87171' }}>{difficulty?.hard?.total || 0}</span>
              </p>
            </div>
          </div>

          {/* Database Table Inspector Section */}
          <div style={{ background: '#1e293b', padding: '24px', borderRadius: '12px', border: '1px solid #334155', marginBottom: '32px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h2 style={{ color: '#38bdf8', margin: 0, fontSize: '18px' }}>
                🗄️ Database Design Table Inspector (10 Core Tables)
              </h2>
              <div style={{ fontSize: '13px', color: '#94a3b8' }}>
                Fetched <b>{totalRecords.toLocaleString()}</b> total records for table <b>{selectedTable}</b>
              </div>
            </div>

            {/* Table Selector Buttons */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '20px' }}>
              {tablesSummary.map(t => (
                <button
                  key={t.table_name}
                  onClick={() => setSelectedTable(t.table_name)}
                  style={{
                    padding: '8px 14px',
                    borderRadius: '8px',
                    border: '1px solid',
                    borderColor: selectedTable === t.table_name ? '#38bdf8' : '#475569',
                    background: selectedTable === t.table_name ? '#0284c7' : '#0f172a',
                    color: '#f8fafc',
                    cursor: 'pointer',
                    fontWeight: selectedTable === t.table_name ? 'bold' : 'normal',
                    fontSize: '13px'
                  }}
                >
                  {t.table_name} ({t.row_count.toLocaleString()})
                </button>
              ))}
            </div>

            {/* Table Data View */}
            <div style={{ overflowX: 'auto', maxHeight: '450px', borderRadius: '8px', border: '1px solid #334155' }}>
              {tableLoading ? (
                <p style={{ padding: '20px', color: '#94a3b8', margin: 0 }}>Loading all {selectedTable} table records...</p>
              ) : tableData.length === 0 ? (
                <p style={{ padding: '20px', color: '#94a3b8', margin: 0 }}>No records in table <b>{selectedTable}</b> yet.</p>
              ) : (
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
                  <thead>
                    <tr style={{ background: '#0f172a', borderBottom: '1px solid #334155' }}>
                      {getTableColumns().map(col => (
                        <th key={col} style={{ padding: '10px 14px', color: '#38bdf8', whiteSpace: 'nowrap' }}>{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {paginatedData.map((row, idx) => (
                      <tr key={idx} style={{ borderBottom: '1px solid #334155', background: idx % 2 === 0 ? '#1e293b' : '#0f172a' }}>
                        {getTableColumns().map(col => (
                          <td key={col} style={{ padding: '8px 14px', whiteSpace: 'nowrap', color: '#cbd5e1' }}>
                            {row[col] !== null ? String(row[col]) : <span style={{ color: '#64748b' }}>null</span>}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>

            {/* Pagination Controls */}
            {totalPages > 1 && (
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '16px', fontSize: '13px', color: '#94a3b8' }}>
                <div>
                  Showing {((page - 1) * pageSize + 1).toLocaleString()} – {Math.min(page * pageSize, totalRecords).toLocaleString()} of {totalRecords.toLocaleString()} records
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button
                    disabled={page === 1}
                    onClick={() => setPage(p => Math.max(1, p - 1))}
                    style={{ padding: '6px 12px', background: '#0f172a', border: '1px solid #334155', color: '#f8fafc', borderRadius: '6px', cursor: page === 1 ? 'not-allowed' : 'pointer' }}
                  >
                    ◀ Previous
                  </button>
                  <span style={{ padding: '6px 12px', color: '#38bdf8', fontWeight: 'bold' }}>Page {page} of {totalPages}</span>
                  <button
                    disabled={page === totalPages}
                    onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                    style={{ padding: '6px 12px', background: '#0f172a', border: '1px solid #334155', color: '#f8fafc', borderRadius: '6px', cursor: page === totalPages ? 'not-allowed' : 'pointer' }}
                  >
                    Next ▶
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Highcharts Chart */}
          <div style={{ background: '#1e293b', padding: '24px', borderRadius: '12px', border: '1px solid #334155' }}>
            <HighchartsReact highcharts={Highcharts} options={difficultyChartOptions} />
          </div>
        </>
      )}
    </div>
  );
}
