import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import React from 'react';

interface GraphProps {
  cpu_usage?: number;
  memory_usage?: number;
  errors_by_type?: Record<string, number>;
  success_requests?: number;
  failed_requests?: number;
  tipo: string;
}

const Graph: React.FC<GraphProps> = ({ cpu_usage, memory_usage, errors_by_type, success_requests, failed_requests, tipo }) => {
  const options: Highcharts.Options = {
    title: { text: 'Métricas' },
    chart: { type: tipo },
    series: [],
  };

  if (cpu_usage !== undefined && memory_usage !== undefined) {
    options.series = [
      { name: 'Uso de CPU (%)', data: [cpu_usage] },
      { name: 'Uso de Memória (%)', data: [memory_usage] }
    ];
  } else if (errors_by_type) {
    options.series = [
      {
        name: 'Erros',
        data: Object.entries(errors_by_type).map(([error, count]) => ({ name: error, y: count })),
        type: 'pie'
      }
    ];
  } else if (success_requests !== undefined && failed_requests !== undefined) {
    options.series = [
      { name: 'Bem-sucedidas', data: [success_requests] },
      { name: 'Falhas', data: [failed_requests] }
    ];
  }

  return (
    <div className="p-4">
    <HighchartsReact highcharts={Highcharts} options={options} />
  </div>
  );
};

export default Graph;