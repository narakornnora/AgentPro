import React from 'react';
import { cn } from '@/lib/utils';

interface ModalProps {
  className?: string;
  children?: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({
  className,
  children,
  ...props
}) => {
  return (
    <div className={cn('', className)} {...props}>
      {Modal Component}
      {children}
    </div>
  );
};

export default Modal;
