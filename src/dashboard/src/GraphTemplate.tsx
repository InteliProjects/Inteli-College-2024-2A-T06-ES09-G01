import "./GraphTemplate.css";
import Graph from "./Graph";
import { useEffect, useState } from "react";
import RealtimeGraph from "./RealTimeGraph";

interface Metrics {
  errors_by_type: Record<string, number>;
  cpu_usage: number;
  memory_usage: number;
  success_requests: number;
  failed_requests: number;
  average_response_time: number;
  total_requests: number;
}

function GraphTemplate() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);

  const fetchMetrics = async () => {
    try {
      const response = await fetch("http://localhost:5000/metrics");
      const data = await response.json();
      setMetrics(data);
    } catch (error) {
      console.error("Erro ao buscar métricas: ", error);
    }
  };

  useEffect(() => {
    const interval = setInterval(fetchMetrics, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="row bg-light">
      <div className="col-sm-6">
        <div className="chart-box p-3 shadow rounded">
          <h5 className="text-center">CPU e Memória</h5>
          <RealtimeGraph />
        </div>
      </div>

      <div className="col-sm-6">
        <div className="chart-box p-3 shadow rounded">
          <h5 className="text-center">Distribuição de Erros</h5>
          {metrics && <Graph errors_by_type={metrics.errors_by_type} tipo="pie" />}
        </div>
      </div>

      <div className="col-sm-6 mt-4">
        <div className="chart-box p-3 shadow rounded">
          <h5 className="text-center">Requisições Bem-sucedidas vs Falhas</h5>
          {metrics && (
            <Graph 
              success_requests={metrics.success_requests}
              failed_requests={metrics.failed_requests}
              tipo="column"
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default GraphTemplate;