import { useState, useRef } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Student from './Student'
import Card from './Card'

function App() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setAnalysisResult(null);

    const formData = new FormData();
    formData.append('image', file);

    try {
      // Use relative URL for production, localhost for development
      const apiUrl = process.env.NODE_ENV === 'production' 
        ? '/api/analyze' 
        : 'http://localhost:7777/analyze';
        
      const response = await fetch(apiUrl, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setAnalysisResult(result);
    } catch (err) {
      setError(`Failed to analyze image: ${err.message}`);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className='min-h-screen bg-blue-50 p-8 flex items-center justify-center'>
      <div className='flex flex-col gap-6 justify-center items-center max-w-4xl w-full'>
        {/* Upload Section */}
        <div className='bg-white rounded-xl shadow-md p-6 w-full hover:shadow-2xl transition-all duration-300'>
          <div 
            className='border-2 border-dashed border-blue-600 p-8 rounded-lg flex flex-col items-center justify-center hover:border-blue-800 hover:bg-blue-50 transition-all duration-300 cursor-pointer group'
            onClick={handleBrowseClick}
          >
            <img 
              src="./picture.png" 
              className='h-20 w-20 mb-2 group-hover:scale-110 transition-transform duration-300' 
              alt="" 
            />
            <p className='text-gray-600 text-lg text-center font-semibold group-hover:text-gray-800 transition-colors duration-300'>
              <span className='text-blue-600 group-hover:text-blue-800'>Browse</span> your image here
            </p>
            {loading && (
              <div className='mt-4'>
                <div className='animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600'></div>
                <p className='text-sm text-gray-500 mt-2'>Analyzing image...</p>
              </div>
            )}
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            className="hidden"
          />
        </div>

        {/* Error Display */}
        {error && (
          <div className='bg-red-50 border border-red-200 rounded-xl p-4 w-full'>
            <p className='text-red-600'>{error}</p>
          </div>
        )}

        {/* Results Section */}
        {analysisResult && (
          <div className='bg-white rounded-xl shadow-md p-6 w-full'>
            <h2 className='text-2xl font-bold text-gray-800 mb-6 text-center'>
              🤖 BizPilot AI Analysis
            </h2>
            
            {/* Items Section */}
            <div className='mb-6'>
              <h3 className='text-lg font-semibold text-gray-700 mb-3'>📦 Items Detected</h3>
              <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
                {analysisResult.items?.map((item, index) => (
                  <div key={index} className='bg-blue-50 rounded-lg p-4 border border-blue-200'>
                    <h4 className='font-medium text-gray-800'>{item.name}</h4>
                    <p className='text-blue-600 font-bold'>Count: {item.estimated_count}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Quality Assessment */}
            {analysisResult.quality_assessment && (
              <div className='mb-6'>
                <h3 className='text-lg font-semibold text-gray-700 mb-3'>⭐ Quality Assessment</h3>
                <div className='bg-green-50 rounded-lg p-4 border border-green-200'>
                  <div className='flex items-center mb-2'>
                    <span className='font-medium text-gray-800 mr-2'>Rating:</span>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      analysisResult.quality_assessment.rating === 'Excellent' ? 'bg-green-200 text-green-800' :
                      analysisResult.quality_assessment.rating === 'Good' ? 'bg-blue-200 text-blue-800' :
                      analysisResult.quality_assessment.rating === 'Fair' ? 'bg-yellow-200 text-yellow-800' :
                      'bg-red-200 text-red-800'
                    }`}>
                      {analysisResult.quality_assessment.rating}
                    </span>
                  </div>
                  <p className='text-gray-700 text-sm leading-relaxed'>
                    {analysisResult.quality_assessment.notes}
                  </p>
                </div>
              </div>
            )}

            {/* Optimizations */}
            {analysisResult.optimizations && (
              <div className='mb-6'>
                <h3 className='text-lg font-semibold text-gray-700 mb-3'>💡 Optimization Suggestions</h3>
                <div className='space-y-3'>
                  {analysisResult.optimizations.map((suggestion, index) => (
                    <div key={index} className='bg-yellow-50 rounded-lg p-4 border border-yellow-200'>
                      <p className='text-gray-700 text-sm leading-relaxed'>
                        <span className='font-medium text-yellow-800'>#{index + 1}:</span> {suggestion}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App