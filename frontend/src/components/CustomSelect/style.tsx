import styled from "@emotion/styled";
import { FormControl } from "@mui/material";

export const StyledFormControl = styled(FormControl)(({ theme }) => ({
  "& .MuiInputLabel-root": {
    position: "relative",
    transform: "none",
  },
  "& legend": {
    width: "0.01px",
  },
}));
