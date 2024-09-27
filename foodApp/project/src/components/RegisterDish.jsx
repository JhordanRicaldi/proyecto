"use client"

import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Camera, Plus, X, Star } from 'lucide-react';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { db, storage } from '../firebase';
import { collection, addDoc } from 'firebase/firestore';
import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';

ChartJS.register(ArcElement, Tooltip, Legend);

const ModernAlert = ({ isOpen, onClose, onConfirm, message }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" id="my-modal">
      <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div className="mt-3 text-center">
          <h3 className="text-lg leading-6 font-medium text-gray-900">{message}</h3>
          <div className="mt-2 px-7 py-3">
            <p className="text-sm text-gray-500">
              ¿Estás seguro de que quieres guardar este análisis?
            </p>
          </div>
          <div className="items-center px-4 py-3">
            <button
              id="ok-btn"
              className="px-4 py-2 bg-blue-500 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-300"
              onClick={onConfirm}
            >
              Guardar análisis
            </button>
            <button
              id="cancel-btn"
              className="mt-3 px-4 py-2 bg-gray-300 text-gray-800 text-base font-medium rounded-md w-full shadow-sm hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300"
              onClick={onClose}
            >
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default function RegisterDish() {
  const [ingredients, setIngredients] = useState([]);
  const [currentIngredient, setCurrentIngredient] = useState('');
  const [dishName, setDishName] = useState('');
  const [image, setImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [nutritionalInfo, setNutritionalInfo] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isFavorite, setIsFavorite] = useState(false);
  const [isAlertOpen, setIsAlertOpen] = useState(false);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    setImage(file);
    setPreviewUrl(URL.createObjectURL(file));
  }, []);

  const { getRootProps, getInputProps } = useDropzone({ 
    onDrop,
    accept: {'image/*': []},
    multiple: false 
  });

  const handleAddIngredient = () => {
    if (currentIngredient.trim()) {
      setIngredients([...ingredients, currentIngredient.trim()]);
      setCurrentIngredient('');
    }
  };

  const handleRemoveIngredient = (index) => {
    setIngredients(ingredients.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', image);

    try {
      const response = await fetch('https://vercel-flask-dun-nine.vercel.app/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setNutritionalInfo({
        proteins: Math.round(data.proteins * 100) / 100,
        carbs: Math.round(data.carbs * 100) / 100,
        fats: Math.round(data.fats * 100) / 100,
      });
    } catch (error) {
      console.error('Error:', error);
      alert('Error al analizar la imagen. Por favor, intenta de nuevo.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveToFavorites = () => {
    if (!nutritionalInfo || !dishName || ingredients.length === 0 || !image) {
      alert('Por favor, asegúrate de que todos los campos estén completos.');
      return;
    }

    setIsAlertOpen(true);
  };

  const confirmSaveToFavorites = async () => {
    setIsLoading(true);
    setIsAlertOpen(false);

    try {
      // Subir la imagen a Firebase Storage
      const storageRef = ref(storage, `dish-images/${Date.now()}_${image.name}`);
      await uploadBytes(storageRef, image);
      const imageUrl = await getDownloadURL(storageRef);

      // Guardar los datos del plato en Firestore
      const docRef = await addDoc(collection(db, 'favorites'), {
        dishName,
        ingredients,
        nutritionalInfo,
        imageUrl,
        createdAt: new Date()
      });

      alert('Plato guardado como favorito exitosamente!');
      setIsFavorite(true);
    } catch (error) {
      console.error('Error al guardar el plato:', error);
      alert('Hubo un error al guardar el plato. Por favor, intenta de nuevo.');
    } finally {
      setIsLoading(false);
    }
  };

  const renderNutritionalChart = (label, value, color) => {
    const data = {
      labels: [label, ''],
      datasets: [
        {
          data: [value, 100 - value],
          backgroundColor: [color, '#E5E7EB'],
          borderColor: ['transparent', 'transparent'],
          borderWidth: 1,
        },
      ],
    };

    const options = {
      cutout: '70%',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          enabled: false,
        },
      },
    };

    return (
      <div className="relative w-24 h-24">
        <Doughnut data={data} options={options} />
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-lg font-bold">{value}%</span>
        </div>
      </div>
    );
  };

  return (
    <div className="container mx-auto p-6 bg-white shadow-lg rounded-xl max-w-6xl">
      <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">Registra tu plato</h1>
      <div className="flex flex-col md:flex-row gap-8 mt-6">
        <div className="md:w-1/2">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block mb-2 font-medium text-gray-700">Nombre del plato:</label>
              <input
                type="text"
                value={dishName}
                onChange={(e) => setDishName(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                placeholder="Ej: Ensalada César"
              />
            </div>
            <div>
              <label className="block mb-2 font-medium text-gray-700">Ingredientes:</label>
              <div className="flex">
                <input
                  type="text"
                  value={currentIngredient}
                  onChange={(e) => setCurrentIngredient(e.target.value)}
                  className="flex-grow p-3 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                  placeholder="Ej: Pollo"
                />
                <button
                  type="button"
                  onClick={handleAddIngredient}
                  className="bg-blue-600 text-white p-3 rounded-r-lg hover:bg-blue-700 transition focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  <Plus size={24} />
                </button>
              </div>
              <div className="mt-2 overflow-x-auto scrollbar-thin scrollbar-thumb-blue-500 scrollbar-track-blue-100">
                <div className="flex space-x-2 pb-2">
                  {ingredients.map((ingredient, index) => (
                    <div key={index} className="flex items-center bg-gray-100 p-2 rounded whitespace-nowrap">
                      <span>{ingredient}</span>
                      <button
                        type="button"
                        onClick={() => handleRemoveIngredient(index)}
                        className="ml-2 text-red-500 hover:text-red-700"
                      >
                        <X size={18} />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div 
              {...getRootProps()} 
              className="border-2 border-dashed border-gray-400 rounded-lg p-6 text-center cursor-pointer hover:bg-gray-50 transition"
            >
              <input {...getInputProps()} />
              {previewUrl ? (
                <img src={previewUrl} alt="Preview" className="mx-auto max-h-48 object-contain" />
              ) : (
                <>
                  <Camera className="mx-auto mb-4 text-gray-400" size={48} />
                  <p className="text-gray-500">Arrastra y suelta una imagen aquí, o haz clic para seleccionar una</p>
                </>
              )}
            </div>
            <button 
              type="submit" 
              className="w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed"
              disabled={!image || isLoading}
            >
              {isLoading ? 'Analizando...' : 'Analizar'}
            </button>
          </form>
        </div>
        <div className="md:w-1/2">
          {nutritionalInfo && (
            <div className="mt-8 p-4 bg-gray-50 rounded-lg shadow-inner relative">
              <button
                onClick={handleSaveToFavorites}
                className={`absolute top-2 right-2 text-2xl ${isFavorite ? 'text-yellow-500' : 'text-gray-400'}`}
                disabled={isLoading}
              >
                <Star size={24} fill={isFavorite ? 'currentColor' : 'none'} />
              </button>
              <h2 className="text-xl font-bold mb-4 text-gray-800">{dishName || 'Información Nutricional'}</h2>
              <div className="mb-4">
                <h3 className="font-semibold mb-2">Ingredientes:</h3>
                <div className="overflow-x-auto">
                  <table className="min-w-full bg-white">
                    <tbody>
                      {ingredients.map((ingredient, index) => (
                        <tr key={index} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                          <td className="py-2 px-4 border-b border-gray-200">{ingredient}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
              <div className="flex justify-around">
                <div className="text-center">
                  <p className="mb-2 font-semibold">Proteínas</p>
                  {renderNutritionalChart('Proteínas', nutritionalInfo.proteins, '#4299E1')}
                </div>
                <div className="text-center">
                  <p className="mb-2 font-semibold">Carbohidratos</p>
                  {renderNutritionalChart('Carbohidratos', nutritionalInfo.carbs, '#48BB78')}
                </div>
                <div className="text-center">
                  <p className="mb-2 font-semibold">Grasas</p>
                  {renderNutritionalChart('Grasas', nutritionalInfo.fats, '#F6AD55')}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
      <ModernAlert
        isOpen={isAlertOpen}
        onClose={() => setIsAlertOpen(false)}
        onConfirm={confirmSaveToFavorites}
        message="Guardar análisis"
      />
    </div>
  );
}