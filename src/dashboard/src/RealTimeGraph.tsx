import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

const socket = io('http://localhost:5000');

const RealtimeGraph = () => {
  const [cpuData, setCpuData] = useState<number[]>([]);
  const [memoryData, setMemoryData] = useState<number[]>([]);
  const [timestamps, setTimestamps] = useState<string[]>([]);
  const [dataPoints, setDataPoints] = useState<number>(20);

  useEffect(() => {
    socket.on('metrics_update', (data) => {
      console.log(data);

      const receivedTimestamp = data.timestamp
        ? new Date(data.timestamp * 1000).toLocaleString('pt-BR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        })
        : new Date().toLocaleString('pt-BR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        });

      setCpuData((prev) => [...prev, data.cpu_usage]);
      setMemoryData((prev) => [...prev, data.memory_usage]);
      setTimestamps((prev) => [...prev, receivedTimestamp]);
    });

    socket.emit('request_metrics');

    return () => {
      socket.off('metrics_update');
    };
  }, []);

  const handleDataPointsChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = Math.max(1, Math.min(100, Number(event.target.value)));
    setDataPoints(value);
  };

  const displayedCpuData = cpuData.slice(-dataPoints);
  const displayedMemoryData = memoryData.slice(-dataPoints);
  const displayedTimestamps = timestamps.slice(-dataPoints);

  const options = {
    title: { text: 'Uso de CPU e Memória (Tempo Real)' },
    xAxis: {
      categories: displayedTimestamps,
      title: { text: 'Horário' }
    },
    yAxis: {
      title: { text: 'Uso (%)' }
    },
    series: [
      { name: 'CPU (%)', data: displayedCpuData },
      { name: 'Memória (%)', data: displayedMemoryData },
    ],
  };

  return (
    <div className="p-4">
      <div className="mb-4">
        <label className="block text-lg font-semibold mb-2">
          Número de dados a serem exibidos:
        </label>
        {' '}
        <input
          type="number"
          value={dataPoints}
          onChange={handleDataPointsChange}
          min={1}
          max={100}
          className="w-20 px-1 rounded border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
        />
      </div>
      <HighchartsReact highcharts={Highcharts} options={options} />
    </div>
  );
};

export default RealtimeGraph;