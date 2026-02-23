import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './BaseStation.css'
import BaseStation from './BaseStation.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BaseStation/>
  </StrictMode>
)
