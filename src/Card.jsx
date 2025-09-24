function Card(){
    return(
        <div className="max-w-sm mx-auto p-8 bg-white dark:bg-gray-800 rounded-xl shadow-md space-y-2 sm:flex sm:items-center sm:py-4 sm:space-y-0 sm:space-x-6 sm:flex-shrink-0 gap-3">
            <img className="h-24 w-24 mx-auto rounded-full ring-4 ring-green-200 sm:mx-0 hover:scale-105 duration-500" 
                 src="/youtube.png" 
                 alt="YouTube Channel"
                 onError={(e) => console.log('Image failed to load:', e)}
                 onLoad={() => console.log('Image loaded successfully')}/>        
            <div className="text-center space-y-2 sm:text-left">
                <div className="space-y-0.5">
                    <h1 className="text-lg text-black dark:text-white font-semibold">Learn with Utshav</h1>
                    <p className="text-gray-500 dark:text-gray-400 font-medium">YouTube Channel</p>
                </div>

                <div className="space-x-2">
                    <button className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors">Visit Now</button>
                    <button className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors">Website</button>
                </div>
            </div>
        </div>
    );
}

export default Card