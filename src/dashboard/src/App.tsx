import Header from './Header.tsx'
import Dashboard from './Dashboard.tsx'

function App() {
  return (
    <div className='container'>
      <div className='row'>
        <div className='col'>
          <Header/>
          <Dashboard/>
          {/* <Footer/> */}
        </div>
      </div>
    </div>
  )
}

export default App