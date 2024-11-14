import { useEffect, useState } from 'react';
import './Kpi.css';

function Kpi() {
  const [kpiData, setKpiData] = useState({
    kpi1: 0,
    kpi2: 0,
    kpi3: 0,
    kpi4: 0
  });

  useEffect(() => {
    const fetchKpiData = async () => {
      try {
        const response = await fetch('http://localhost:5000/metrics');
        const data = await response.json();

        setKpiData({
          kpi1: data.success_requests, 
          kpi2: data.failed_requests,  
          kpi3: data.average_response_time.toFixed(2),  
          kpi4: (data.cpu_usage + data.memory_usage).toFixed(2)  
        });
      } catch (error) {
        console.error('Erro ao buscar os dados das KPIs:', error);
      }
    };

    fetchKpiData();
    const interval = setInterval(fetchKpiData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="row text-center mb-4">
      <div className="col-sm-3">
        <div className="kpi-box kpi-success p-3 shadow rounded">
          <h6>Requisições Bem-Sucedidas</h6>
          <p>{kpiData.kpi1}</p>
        </div>
      </div>
      <div className="col-sm-3">
        <div className="kpi-box kpi-failed p-3 shadow rounded">
          <h6>Requisições Falhadas</h6>
          <p>{kpiData.kpi2}</p>
        </div>
      </div>
      <div className="col-sm-3">
        <div className="kpi-box kpi-response p-3 shadow rounded">
          <h6>Tempo Médio de Resposta</h6>
          <p>{kpiData.kpi3} s</p>
        </div>
      </div>
      <div className="col-sm-3">
        <div className="kpi-box kpi-resource p-3 shadow rounded">
          <h6>Uso de CPU e Memória</h6>
          <p>{kpiData.kpi4} %</p>
        </div>
      </div>
    </div>
  );
}

export default Kpi;