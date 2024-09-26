import React from 'react'

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import HomePage from './components/HomePage'
import RegisterDish from './components/RegisterDish'
import NutritionalAnalysis from './components/NutritionalAnalysis'
import DishHistory from './components/DishHistory'
import Favorites from './components/Favorites'
import Recommendations from './components/Recommendations'
import Recipes from './components/Recipes'

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 pt-12">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/register" element={<RegisterDish />} />
          <Route path="/analysis" element={<NutritionalAnalysis />} />
          <Route path="/history" element={<DishHistory />} />
          <Route path="/favorites" element={<Favorites />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/recipes" element={<Recipes />} />
        </Routes>
      </div>
    </Router>
  )
}
