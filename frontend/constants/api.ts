const getApiUrl = (): string => {
  const url = process.env.NEXT_PUBLIC_API_URL;
  
  if (!url) {
    throw new Error('NEXT_PUBLIC_API_URL environment variable must be defined. Please set it in your .env.local file.');
  }
  
  return url;
};

export const API_URL = getApiUrl();


