import { useEffect, useState } from 'react';
import './Logs.css';

interface Metrics {
  average_response_time: number;
  cpu_usage: number;
  memory_usage: number;
  total_requests: number;
  success_requests: number;
  failed_requests: number;
  errors_by_type: Record<string, number>;
}

const Logs = () => {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await fetch('http://localhost:5000/metrics');
        const data = await response.json();
        setMetrics(data);
      } catch (error) {
        console.error('Error fetching metrics:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();

    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!metrics) {
    return <div>No metrics data available</div>;
  }

  return (
    <div className="row log-container">
      <h2>Logs de Métricas do Servidor</h2>

      <div className="metrics-card">
        <div className="metric">
          <span className="metric-label">Average Response Time:</span>
          <span className="metric-value">{metrics.average_response_time.toFixed(2)} seconds</span>
        </div>
        <div className="metric">
          <span className="metric-label">CPU Usage:</span>
          <span className="metric-value">{metrics.cpu_usage}%</span>
        </div>
        <div className="metric">
          <span className="metric-label">Memory Usage:</span>
          <span className="metric-value">{metrics.memory_usage}%</span>
        </div>
        <div className="metric">
          <span className="metric-label">Total Requests:</span>
          <span className="metric-value">{metrics.total_requests}</span>
        </div>
        <div className="metric">
          <span className="metric-label">Success Requests:</span>
          <span className="metric-value">{metrics.success_requests}</span>
        </div>
        <div className="metric">
          <span className="metric-label">Failed Requests:</span>
          <span className="metric-value">{metrics.failed_requests}</span>
        </div>
        <br />
        <h3>Errors by Type</h3>
        <ul className="error-list">
          {Object.entries(metrics.errors_by_type).map(([errorType, count]) => (
            <li key={errorType}>
              <strong>{errorType}:</strong> <span className="error-count">{count}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Logs;