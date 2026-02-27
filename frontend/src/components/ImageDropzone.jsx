import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'
import { HiOutlineCloudUpload, HiOutlinePhotograph } from 'react-icons/hi'
import './ImageDropzone.css'

export default function ImageDropzone({ onFileSelect, preview, disabled }) {
  const onDrop = useCallback(
    (accepted) => {
      if (accepted.length > 0) onFileSelect(accepted[0])
    },
    [onFileSelect],
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpg', '.jpeg', '.png', '.webp'] },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024,
    disabled,
  })

  return (
    <motion.div
      className={`dropzone ${isDragActive ? 'dropzone--active' : ''} ${preview ? 'dropzone--has-preview' : ''} ${disabled ? 'dropzone--disabled' : ''}`}
      {...getRootProps()}
      whileHover={!disabled ? { scale: 1.01 } : {}}
      whileTap={!disabled ? { scale: 0.99 } : {}}
    >
      <input {...getInputProps()} aria-label="Upload food image" />

      {preview ? (
        <div className="dropzone__preview">
          <img src={preview} alt="Preview of uploaded food" className="dropzone__image" />
          <div className="dropzone__overlay">
            <HiOutlinePhotograph size={28} />
            <span>Click or drop to change image</span>
          </div>
        </div>
      ) : (
        <div className="dropzone__placeholder">
          <motion.div
            className="dropzone__icon"
            animate={isDragActive ? { scale: 1.15, y: -5 } : { scale: 1, y: 0 }}
            transition={{ type: 'spring', stiffness: 300 }}
          >
            <HiOutlineCloudUpload size={48} />
          </motion.div>
          <h3 className="dropzone__title">
            {isDragActive ? 'Drop your image here' : 'Upload Food Image'}
          </h3>
          <p className="dropzone__desc">
            Drag &amp; drop or <span className="dropzone__browse">browse</span> to upload
          </p>
          <p className="dropzone__hint">JPG, PNG or WebP — max 10 MB</p>

          <div className="dropzone__tip">
            <span className="dropzone__tip-icon">👍</span>
            <span>Include your <strong>thumb</strong> next to the food for accurate size calibration</span>
          </div>
        </div>
      )}
    </motion.div>
  )
}
