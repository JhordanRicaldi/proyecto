import React from 'react'
import { Link } from 'react-router-dom'

export default function HomePage() {
  return (
    <div className="relative h-screen bg-cover bg-center" style={{backgroundImage: "url('/path-to-your-food-image.jpg')"}}>
      <div className="absolute inset-0 bg-black opacity-50"></div>
      <div className="relative z-10 flex flex-col items-center justify-center h-full text-white">
        <h1 className="text-5xl font-bold mb-4">Descubre tu nutrición</h1>
        <p className="text-xl mb-8">Analiza tus platos y mejora tu dieta</p>
        <Link to="/register" className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
          Comienza
        </Link>
      </div>
    </div>
  )
}