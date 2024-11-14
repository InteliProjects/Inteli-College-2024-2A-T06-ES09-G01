import './Dashboard.css';
import GraphTemplate from './GraphTemplate';
import Kpi from './Kpi';
import Logs from './Logs';

function Dashboard() {
  return (
    <div>
      <div className="row">
        <div className='col bg-light'>
            <Kpi/>
        </div>
      </div>
      <GraphTemplate/>
      <Logs />
    </div>
  );
}

export default Dashboard;