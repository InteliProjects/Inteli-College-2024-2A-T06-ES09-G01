function Header() {
    return (
        <div className='row bg-light justify-content-between'>
            <div className='col'>
                <header className="navbar navbar-expand-md navbar-light justify-content-between">
                    <a className="navbar-brand mt-2 mx-2 pt-2" href="#"><h2 className='mb-n1'>Controle de Qualidade Cogny</h2></a>
                    <img src="https://appexchange.salesforce.com/partners/servlet/servlet.FileDownload?file=00P4V000012wQ06UAE" alt="cogny" className="align-self-end" width={50}/>
                </header>
                <hr className='pb-3'/>
            </div>
        </div>
    );
}

export default Header