/**
 * FilePreview Component
 * 
 * Displays uploaded file thumbnail with remove functionality
 */

'use client';

interface FilePreviewProps {
  /** Preview URL for the image */
  previewUrl: string;
  /** Callback when remove button is clicked */
  onRemove: () => void;
}

export function FilePreview({ previewUrl, onRemove }: FilePreviewProps) {
  return (
    <div className="relative w-20 h-20 rounded-3xl overflow-hidden bg-neutral-100 group">
      <img 
        src={previewUrl} 
        alt="Reference file preview"
        className="w-full h-full object-cover"
      />
      <button
        type="button"
        onClick={onRemove}
        className="absolute inset-0 flex items-center justify-center bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity"
        aria-label="Remove file"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="w-6 h-6 text-white"
          aria-hidden="true"
        >
          <circle cx="12" cy="12" r="10"></circle>
          <path d="m15 9-6 6"></path>
          <path d="m9 9 6 6"></path>
        </svg>
      </button>
    </div>
  );
}
