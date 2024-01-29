import { useState } from 'react';
import '../App.css';
import placeholderImage from '../visitantes/Placeholder.jpg'; // Importar la imagen de placeholder
const uuid = require('uuid');

function EntryExitMonitorLog(){

    const [image, setImage] = useState('');
    const [mensajeDeCarga, setMensajeDeCarga] = useState('Por favor suba una imagen para verificar su identidad');
    const [autentificado, Setautentificado] = useState(false);
    const [visitorImageName, setVisitorImageName] = useState('placeholder');
    const [tenantId, setTenantId] = useState(''); // Estado para tenantId
    const [modoIngreso, setModoIngreso] = useState('Entrada'); // Estado para el modo de ingreso

    function sendImage(e){
      e.preventDefault();
      if (!tenantId) {
          setMensajeDeCarga('Por favor ingrese el Tenant ID.');
          return; // Detiene la ejecución si no hay tenantId
      }
      const newVisitorImageName = `${uuid.v4()}_${modoIngreso}_${tenantId}`; // Incluir tenantId y modo de ingreso en el nombre del archivo

      fetch(`https://ed32u8vxs7.execute-api.us-east-1.amazonaws.com/dev/visitantes-temporales/${newVisitorImageName}.jpeg`,
      {
        method:'PUT', 
        headers: {
          'Content-Type':'image/jpeg'
        },
        body: image
      }
      ).then(async ()=> {
        setVisitorImageName(newVisitorImageName); // Actualizar el nombre solo después de subir la imagen
        const response = await authenticate(newVisitorImageName);
        if(response.Message === 'EXITO'){
          Setautentificado(true)
          setMensajeDeCarga(`Hola ${response['firstname']} ${response['lastname']} ha sido autorizado(@) ...`)
        } else {
          Setautentificado(false)
          setMensajeDeCarga('Acceso no autorizado') 
        }
  
      }).catch(
        error => { 
          Setautentificado(false);
          setMensajeDeCarga('NO HAY RESPUESTA DEL SISTEMA ESPERE UN MOMENTO ...')
          console.log(error);
        });
    }
   
    async function authenticate(visitorImageName) {
      const requestUrl = 'https://ed32u8vxs7.execute-api.us-east-1.amazonaws.com/dev/empleado?' + new URLSearchParams({
        objectKey: `${visitorImageName}.jpeg`
      });
    
      return await fetch(requestUrl, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        }
      }).then(response => response.json())
        .then(data => {
          return data;
        }).catch(error => console.error(error));
    }
    
    const imageUrl = visitorImageName === 'placeholder' 
                     ? placeholderImage
                     : `https://visitantes-temporales.s3.amazonaws.com/${visitorImageName}.jpeg`;
  
    return (
      <div className="App">
        <h2>Sistema de verificación de identidad </h2>
        <form onSubmit={sendImage}>
          <input type='file' name='image' onChange={e => setImage(e.target.files[0])}/>
          <input type='text' name='tenantId' placeholder='Ingrese Tenant ID' onChange={e => setTenantId(e.target.value)} required/>
          <select name='modoIngreso' onChange={e => setModoIngreso(e.target.value)} defaultValue='Entrada'>
            <option value='Entrada'>Entrada</option>
            <option value='Salida'>Salida</option>
          </select>
          <button type='submit'> Autentificar identidad </button>
        </form>
        <div className={autentificado ? 'success' : 'failure'}>
          {mensajeDeCarga}
        </div>
        <img src={imageUrl} alt="Visitante" height={250} width={250}/>
      </div>
    );
}

export default EntryExitMonitorLog;
